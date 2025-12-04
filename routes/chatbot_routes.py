"""
Chatbot Routes - Enhanced chatbot for admission queries
"""
from flask import Blueprint, request, jsonify, session
from utils.db_helper import get_db_connection
from utils.chatbot_handler import ChatbotHandler
import uuid

bp = Blueprint('chatbot', __name__, url_prefix='/chatbot')

@bp.route('/message', methods=['POST'])
def handle_message():
    """Handle chatbot messages"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        
        if not message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Get or create session ID
        if 'chatbot_session_id' not in session:
            session['chatbot_session_id'] = str(uuid.uuid4())
        
        session_id = session['chatbot_session_id']
        
        conn = get_db_connection()
        if not conn:
            return jsonify({
                'response': 'I apologize, but I\'m having trouble connecting to the database. Please try again later.',
                'session_id': session_id
            }), 200
        
        handler = ChatbotHandler(conn)
        response = handler.process_message(message, session_id)
        
        conn.close()
        
        return jsonify({
            'response': response['message'],
            'session_id': session_id,
            'suggestions': response.get('suggestions', []),
            'intent': response.get('intent', 'general')
        }), 200
        
    except Exception as e:
        return jsonify({
            'response': f'I encountered an error: {str(e)}. Please try rephrasing your question.',
            'error': str(e)
        }), 200

@bp.route('/session', methods=['GET'])
def get_session():
    """Get or create chatbot session"""
    if 'chatbot_session_id' not in session:
        session['chatbot_session_id'] = str(uuid.uuid4())
    
    return jsonify({
        'session_id': session['chatbot_session_id']
    }), 200

@bp.route('/history', methods=['GET'])
def get_history():
    """Get chat history for current session"""
    if 'chatbot_session_id' not in session:
        return jsonify({'messages': []}), 200
    
    session_id = session['chatbot_session_id']
    
    conn = get_db_connection()
    if not conn:
        return jsonify({'messages': []}), 200
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT cs.session_id
            FROM CHAT_SESSION cs
            WHERE cs.session_id = %s
            LIMIT 1
        """, (session_id,))
        
        session_record = cursor.fetchone()
        
        if session_record:
            cursor.execute("""
                SELECT sender_type, message_text, timestamp, intent_detected
                FROM CHAT_MESSAGE
                WHERE session_id = %s
                ORDER BY timestamp ASC
            """, (session_record['session_id'],))
            messages = cursor.fetchall()
        else:
            messages = []
        
        cursor.close()
        conn.close()
        
        return jsonify({'messages': messages}), 200
        
    except Exception as e:
        if conn:
            conn.close()
        return jsonify({'messages': [], 'error': str(e)}), 200


