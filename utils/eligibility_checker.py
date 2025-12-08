"""
Eligibility Checker - NLP-like matching for admission requirements
"""
import re
from datetime import datetime

class EligibilityChecker:
    """Check applicant eligibility against program requirements using NLP-like matching"""
    
    def __init__(self, db_connection):
        self.conn = db_connection
        
        # Qualification equivalency mapping
        self.qualification_equivalents = {
            'stpm': ['stpm', 'sijil tinggi persekolahan malaysia', 'higher school certificate'],
            'a-level': ['a-level', 'a level', 'gce a-level', 'advanced level'],
            'uec': ['uec', 'unified examination certificate', 'unified exam'],
            'diploma': ['diploma', 'diploma level'],
            'foundation': ['foundation', 'foundation studies', 'pre-university'],
            'matriculation': ['matriculation', 'matrikulasi', 'matric'],
            'spm': ['spm', 'sijil pelajaran malaysia', 'malaysian certificate of education']
        }
        
        # Grade equivalency mapping
        self.grade_equivalents = {
            'a+': 4.0, 'a': 4.0, 'a-': 3.67,
            'b+': 3.33, 'b': 3.0, 'b-': 2.67,
            'c+': 2.33, 'c': 2.0, 'c-': 1.67,
            'd+': 1.33, 'd': 1.0, 'd-': 0.67,
            'e': 0.5, 'f': 0.0
        }
    
    def normalize_qualification(self, qualification):
        """Normalize qualification name for matching"""
        qual_lower = qualification.lower().strip()
        
        for key, variants in self.qualification_equivalents.items():
            if any(variant in qual_lower for variant in variants):
                return key
        
        return qual_lower
    
    def parse_grade(self, grade_input):
        """Parse grade input (CGPA, letter grade, etc.)"""
        if not grade_input:
            return None
        
        grade_str = str(grade_input).strip().upper()
        
        # Try to extract CGPA (decimal number)
        cgpa_match = re.search(r'(\d+\.?\d*)', grade_str)
        if cgpa_match:
            try:
                return float(cgpa_match.group(1))
            except:
                pass
        
        # Try letter grade
        if grade_str in self.grade_equivalents:
            return self.grade_equivalents[grade_str]
        
        # Try to match letter grade pattern
        letter_match = re.search(r'([A-F][+-]?)', grade_str)
        if letter_match:
            letter = letter_match.group(1).upper()
            if letter in self.grade_equivalents:
                return self.grade_equivalents[letter]
        
        return None
    
    def extract_keywords(self, text):
        """Extract keywords from text for matching"""
        if not text:
            return []
        
        # Common academic keywords
        keywords = ['mathematics', 'math', 'english', 'physics', 'chemistry',
                   'biology', 'additional mathematics', 'add math', 'science']
        
        text_lower = text.lower()
        found_keywords = [kw for kw in keywords if kw in text_lower]
        
        return found_keywords
    
    def check_eligibility(self, program_id, qualification, grades, additional_info=None):
        """Check if applicant meets program requirements"""
        if additional_info is None:
            additional_info = {}
        
        try:
            cursor = self.conn.cursor(dictionary=True)
            
            # Get program requirements
            cursor.execute("""
                SELECT ar.*, p.program_name, p.level
                FROM ADMISSION_REQUIREMENT ar
                JOIN PROGRAM p ON ar.program_id = p.program_id
                WHERE ar.program_id = %s
            """, (program_id,))
            
            requirements = cursor.fetchall()
            
            if not requirements:
                return {
                    'eligible': False,
                    'message': 'No admission requirements found for this program.',
                    'matched_requirements': [],
                    'missing_requirements': []
                }
            
            program_name = requirements[0]['program_name']
            normalized_qual = self.normalize_qualification(qualification)
            
            # Find matching requirements
            matched_requirements = []
            missing_requirements = []
            best_match = None
            best_score = 0
            
            for req in requirements:
                req_qual = self.normalize_qualification(req['qualification_type'])
                
                # Calculate match score
                score = 0
                
                # Qualification match
                if req_qual == normalized_qual:
                    score += 10
                elif req_qual in normalized_qual or normalized_qual in req_qual:
                    score += 5
                
                # Grade check
                if req['minimum_grade']:
                    required_grade = self.parse_grade(req['minimum_grade'])
                    applicant_grade = self.parse_grade(grades.get('cgpa') or grades.get('grade'))
                    
                    if required_grade and applicant_grade:
                        if applicant_grade >= required_grade:
                            score += 10
                        else:
                            score -= 5
                
                # Additional requirements check
                if req['additional_requirements']:
                    req_keywords = self.extract_keywords(req['additional_requirements'])
                    applicant_info = str(additional_info).lower()
                    
                    for keyword in req_keywords:
                        if keyword in applicant_info:
                            score += 2
                
                if score > best_score:
                    best_score = score
                    best_match = req
                
                if score >= 10:  # Threshold for match
                    matched_requirements.append({
                        'requirement': req,
                        'score': score,
                        'matched': True
                    })
                else:
                    missing_requirements.append({
                        'requirement': req,
                        'score': score,
                        'matched': False
                    })
            
            # Determine eligibility
            eligible = len(matched_requirements) > 0
            
            # Generate response message
            if eligible and best_match:
                message = f"Based on your {qualification} qualification, you appear to meet the requirements for {program_name}."
                
                if best_match['minimum_grade']:
                    message += f" The minimum requirement is {best_match['minimum_grade']}."
                
                if best_match['additional_requirements']:
                    message += f" Additional requirements: {best_match['additional_requirements']}."
            else:
                message = f"Based on your {qualification} qualification, you may not meet the minimum requirements for {program_name}."
                
                if best_match:
                    message += f" Required: {best_match['qualification_type']} with {best_match['minimum_grade'] or 'specified grade'}."
                    if best_match['additional_requirements']:
                        message += f" Additional: {best_match['additional_requirements']}."
                else:
                    message += " Please check the specific requirements for this program."
            
            cursor.close()
            
            return {
                'eligible': eligible,
                'message': message,
                'program_name': program_name,
                'matched_requirements': matched_requirements,
                'missing_requirements': missing_requirements,
                'best_match': best_match,
                'confidence_score': min(best_score / 20.0, 1.0) if best_score > 0 else 0.0
            }
            
        except Exception as e:
            return {
                'eligible': False,
                'message': f'Error checking eligibility: {str(e)}',
                'matched_requirements': [],
                'missing_requirements': []
            }


