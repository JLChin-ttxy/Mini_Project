"""
Dialogflow webhook to return deep links for program-specific pages
"""
from flask import Blueprint, request, jsonify
from utils.db_helper import get_db_connection
import re
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bp = Blueprint('dialogflow_webhook', __name__)

# Simple in-memory cache to avoid repeated DB hits
_program_links_cache = None
_program_names_cache = None


def _normalize_program_name(name: str) -> str:
    """Normalize program name for matching (lowercase, remove extra spaces)"""
    if not name:
        return ""
    # Convert to lowercase, remove extra spaces, strip
    normalized = re.sub(r'\s+', ' ', name.lower().strip())
    return normalized


def _build_program_links(base_url: str):
    """
    Build a mapping of program_name -> {requirements, deadlines, apply, documents}
    using data from the PROGRAM table. base_url should be something like
    https://yourdomain (derived from request.url_root).
    """
    global _program_links_cache, _program_names_cache
    if _program_links_cache is not None:
        return _program_links_cache, _program_names_cache

    conn = get_db_connection()
    if not conn:
        return {}, {}

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT program_id, program_name FROM PROGRAM ORDER BY program_name")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
    except Exception as e:
        logger.error(f"Dialogflow webhook: failed to load programs: {e}")
        return {}, {}

    links = {}
    names_map = {}  # normalized -> original name mapping
    base = base_url.rstrip("/")
    
    for row in rows:
        pid = row["program_id"]
        name = row["program_name"]
        # Create normalized key for case-insensitive matching
        normalized = _normalize_program_name(name)
        
        links[normalized] = {
            "program_id": pid,
            "program_name": name,  # Store original name
            "requirements": f"{base}/admission/requirements?program_id={pid}",
            "deadlines": f"{base}/admission/deadlines?program_id={pid}",
            "apply": f"{base}/admission/application-form?program_id={pid}",
            "documents": f"{base}/admission/document-checklist?program_id={pid}",
        }
        names_map[normalized] = name
    
    _program_links_cache = links
    _program_names_cache = names_map
    logger.info(f"Loaded {len(links)} programs into cache")
    return links, names_map


def _find_program_match(query_name: str, links_map: dict) -> tuple:
    """
    Find the best matching program name.
    Returns (normalized_key, program_data) or (None, None) if not found.
    """
    if not query_name:
        return None, None
    
    normalized_query = _normalize_program_name(query_name)
    
    # Exact match first
    if normalized_query in links_map:
        return normalized_query, links_map[normalized_query]
    
    # Partial match - check if query is contained in any program name
    for key, data in links_map.items():
        if normalized_query in key or key in normalized_query:
            return key, data
    
    # Fuzzy match - remove common words and try again
    query_words = set(normalized_query.split())
    common_words = {'in', 'of', 'the', 'and', 'for', 'to', 'a', 'an'}
    query_words = query_words - common_words
    
    best_match = None
    best_score = 0
    
    for key, data in links_map.items():
        key_words = set(key.split())
        key_words = key_words - common_words
        
        # Count matching words
        matches = len(query_words & key_words)
        if matches > 0 and matches > best_score:
            best_score = matches
            best_match = (key, data)
    
    if best_match:
        return best_match
    
    return None, None


@bp.route('/dialogflow-webhook', methods=['POST'])
def dialogflow_webhook():
    """
    Dialogflow webhook handler:
    - Expects Dialogflow to send parameters.program_name (resolved entity)
      and optional parameters.info_type (requirements/deadlines/apply/documents).
    - Returns the appropriate deep link as fulfillmentText.
    """
    try:
        # Log the incoming request for debugging
        body = request.get_json(silent=True, force=True) or {}
        logger.info(f"Dialogflow webhook received: {body}")
        
        # Extract query result and parameters
        query_result = body.get("queryResult", {})
        params = query_result.get("parameters", {})
        query_text = query_result.get("queryText", "")
        
        # Extract parameters - handle both direct parameter and entity extraction
        program_name = params.get("program_name") or params.get("ProgramName") or params.get("program")
        
        # If program_name is a list (Dialogflow sometimes returns lists), take the first item
        if isinstance(program_name, list):
            program_name = program_name[0] if program_name else None
        
        # Check if program_name is a placeholder/entity reference (Dialogflow sometimes sends these literally)
        if isinstance(program_name, str):
            # Remove entity reference syntax
            if program_name.startswith("{") or program_name.startswith("@") or program_name == "{@program_name}":
                logger.warning(f"Received entity placeholder: {program_name}, will extract from query text")
                program_name = None
        
        # If still no program_name, try to extract from query text
        if not program_name:
            # Try to extract from query text
            if query_text:
                query_lower = query_text.lower()
                # Handle typos and variations
                if "foundation in scien" in query_lower or "foundation in scienece" in query_lower:
                    program_name = "Foundation in Science"
                elif "foundation in science" in query_lower:
                    program_name = "Foundation in Science"
                elif "foundation in art" in query_lower or "foundation in arts" in query_lower:
                    program_name = "Foundation in Arts"
                elif "foundation" in query_lower and "science" in query_lower:
                    program_name = "Foundation in Science"
                elif "foundation" in query_lower and ("art" in query_lower or "arts" in query_lower):
                    program_name = "Foundation in Arts"
                elif "foundation" in query_lower:
                    # Default to Foundation in Science if just "foundation" is mentioned
                    program_name = "Foundation in Science"
                # Try to extract any program name from query text using fuzzy matching
                else:
                    # Get all program names and try to find a match in the query
                    links_map_temp, _ = _build_program_links(request.url_root)
                    matched_key, program_data = _find_program_match(query_text, links_map_temp)
                    if program_data:
                        program_name = program_data.get("program_name")
        
        info_type = params.get("info_type") or params.get("InfoType") or "requirements"
        if isinstance(info_type, list):
            info_type = info_type[0] if info_type else "requirements"
        
        logger.info(f"Extracted - program_name: {program_name}, info_type: {info_type}, query_text: {query_text}")
        
        # Build links (with cached program list) - do this early so we can use it for extraction
        links_map, names_map = _build_program_links(request.url_root)
        
        # Final attempt: if program_name is still missing, extract from query text using fuzzy matching
        if not program_name and query_text:
            logger.info(f"Attempting to extract program name from query text: '{query_text}'")
            matched_key, program_data = _find_program_match(query_text, links_map)
            if program_data:
                program_name = program_data.get("program_name")
                logger.info(f"✅ Successfully extracted program_name from query text: {program_name}")
            else:
                logger.warning(f"❌ Could not extract program name from query text: '{query_text}'")
        
        # Handle queries without program name - provide general information
        if not program_name:
            query_lower = query_text.lower() if query_text else ""
            
            # Check what type of information they're asking for
            if any(word in query_lower for word in ['requirement', 'eligibility', 'qualification', 'need to apply', 'admission criteria']):
                base_url = request.url_root.rstrip("/")
                return jsonify({
                    "fulfillmentText": f"I can help you with admission requirements! Please visit our Admission Requirements page to see requirements for all programs: {base_url}/admission/requirements\n\nOr tell me which specific program you're interested in (e.g., 'Foundation in Science' or 'Bachelor of Computer Science') and I'll show you the exact requirements."
                })
            elif any(word in query_lower for word in ['document', 'checklist', 'need to submit', 'required document', 'paperwork']):
                base_url = request.url_root.rstrip("/")
                return jsonify({
                    "fulfillmentText": f"I can help you with document requirements! Please visit our Document Checklist page: {base_url}/admission/document-checklist\n\nOr tell me which specific program you're applying for (e.g., 'Foundation in Science') and I'll generate a personalized checklist for you."
                })
            elif any(word in query_lower for word in ['deadline', 'when is', 'closing date', 'application period', 'intake']):
                base_url = request.url_root.rstrip("/")
                return jsonify({
                    "fulfillmentText": f"I can help you with important dates and deadlines! Please visit our Important Dates page: {base_url}/admission/deadlines\n\nOr tell me which specific program you're interested in and I'll show you the exact deadlines."
                })
            elif any(word in query_lower for word in ['apply', 'application', 'how to apply', 'application process']):
                base_url = request.url_root.rstrip("/")
                return jsonify({
                    "fulfillmentText": f"I can help you with the application process! Please visit our Application Procedure page: {base_url}/admission/application-procedure\n\nOr tell me which specific program you want to apply for and I'll guide you through the steps."
                })
            else:
                # General response
                return jsonify({
                    "fulfillmentText": "I'd be happy to help! I can assist you with:\n• Admission requirements\n• Document checklists\n• Important dates and deadlines\n• Application procedures\n\nPlease tell me which program you're interested in (e.g., 'Foundation in Science' or 'Bachelor of Computer Science'), or ask me a specific question like 'What are the requirements?' or 'What documents do I need?'"
                })
        
        # Find matching program
        matched_key, program_data = _find_program_match(program_name, links_map)
        
        if not program_data:
            # Return helpful message with suggestions
            available_programs = list(names_map.values())[:5]  # First 5 programs
            suggestions = ", ".join(available_programs)
            return jsonify({
                "fulfillmentText": f"I couldn't find '{program_name}' in our system. Here are some available programs: {suggestions}. Please try asking about one of these programs."
            })
        
        # Determine info_type from query if not provided
        if not info_type or info_type == "requirements":
            query_lower = query_text.lower() if query_text else ""
            if any(word in query_lower for word in ['document', 'checklist', 'paperwork', 'certificate']):
                info_type = "documents"
            elif any(word in query_lower for word in ['deadline', 'date', 'when', 'intake', 'closing']):
                info_type = "deadlines"
            elif any(word in query_lower for word in ['apply', 'application form', 'submit application']):
                info_type = "apply"
            elif any(word in query_lower for word in ['requirement', 'eligibility', 'qualification', 'need to apply']):
                info_type = "requirements"
        
        # Get the appropriate URL
        url = program_data.get(info_type) or program_data.get("requirements")
        original_name = program_data.get("program_name", program_name)
        
        # Create a user-friendly response
        if info_type == "requirements":
            reply = f"Here are the admission requirements for {original_name}: {url}"
        elif info_type == "deadlines":
            reply = f"Here are the important dates and deadlines for {original_name}: {url}"
        elif info_type == "apply":
            reply = f"Here's the application form for {original_name}: {url}"
        elif info_type == "documents":
            reply = f"Here's the document checklist for {original_name}: {url}"
        else:
            reply = f"Here's the information page for {original_name}: {url}"
        
        logger.info(f"Returning response: {reply}")
        
        return jsonify({
            "fulfillmentText": reply
        })
        
    except Exception as e:
        logger.error(f"Error in Dialogflow webhook: {e}", exc_info=True)
        return jsonify({
            "fulfillmentText": "I'm sorry, I encountered an error processing your request. Please try again or contact the admission office for assistance."
        })
