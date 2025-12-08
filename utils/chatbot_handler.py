"""
Chatbot Handler - Process admission-related queries
"""
import re
from datetime import datetime

class ChatbotHandler:
    """Handle chatbot messages with intent detection and response generation"""
    
    def __init__(self, db_connection):
        self.conn = db_connection
        
        # Intent patterns
        self.intent_patterns = {
            'admission_requirements': [
                r'requirement', r'eligibility', r'qualification', r'need to apply',
                r'what do i need', r'admission criteria', r'entry requirement'
            ],
            'application_procedure': [
                r'how to apply', r'application process', r'apply', r'application procedure',
                r'steps to apply', r'application guide', r'how do i apply'
            ],
            'deadlines': [
                r'deadline', r'when is', r'closing date', r'application period',
                r'intake', r'when can i', r'important date', r'due date'
            ],
            'documents': [
                r'document', r'what document', r'checklist', r'need to submit',
                r'required document', r'paperwork', r'certificate'
            ],
            'fees': [
                r'fee', r'tuition', r'cost', r'price', r'how much', r'payment',
                r'scholarship', r'financial aid'
            ],
            'program_info': [
                r'program', r'course', r'what is', r'tell me about', r'information about'
            ]
        }
    
    def detect_intent(self, message):
        """Detect user intent from message"""
        message_lower = message.lower()
        
        intent_scores = {}
        
        for intent, patterns in self.intent_patterns.items():
            score = 0
            for pattern in patterns:
                if re.search(pattern, message_lower):
                    score += 1
            if score > 0:
                intent_scores[intent] = score
        
        if intent_scores:
            return max(intent_scores, key=intent_scores.get)
        return 'general'
    
    def process_message(self, message, session_id):
        """Process chatbot message and generate response"""
        intent = self.detect_intent(message)
        
        # Save message to database
        self._save_message(session_id, 'User', message, intent)
        
        # Generate response based on intent
        response = self._generate_response(message, intent)
        
        # Save bot response
        self._save_message(session_id, 'Bot', response['message'], intent)
        
        return response
    
    def _generate_response(self, message, intent):
        """Generate response based on intent"""
        message_lower = message.lower()
        
        if intent == 'admission_requirements':
            return self._handle_requirements_query(message)
        elif intent == 'application_procedure':
            return self._handle_procedure_query(message)
        elif intent == 'deadlines':
            return self._handle_deadline_query(message)
        elif intent == 'documents':
            return self._handle_document_query(message)
        elif intent == 'fees':
            return self._handle_fee_query(message)
        elif intent == 'program_info':
            return self._handle_program_query(message)
        else:
            return self._handle_general_query(message)
    
    def _handle_requirements_query(self, message):
        """Handle admission requirements queries"""
        try:
            cursor = self.conn.cursor(dictionary=True)
            
            # Try to extract program name
            program_match = re.search(r'(computer|engineering|business|accounting|science|psychology)', message.lower())
            
            if program_match:
                program_keyword = program_match.group(1)
                cursor.execute("""
                    SELECT p.program_id, p.program_name, ar.qualification_type, 
                           ar.minimum_grade, ar.additional_requirements
                    FROM PROGRAM p
                    LEFT JOIN ADMISSION_REQUIREMENT ar ON p.program_id = ar.program_id
                    WHERE p.program_name LIKE %s
                    LIMIT 5
                """, (f'%{program_keyword}%',))
                
                programs = cursor.fetchall()
                
                if programs:
                    program = programs[0]
                    response = f"For {program['program_name']}, the admission requirements include:\n"
                    
                    reqs = [r for r in programs if r['qualification_type']]
                    if reqs:
                        min_grade = reqs[0]['minimum_grade'] or 'equivalent qualification'
                        response += f"• {reqs[0]['qualification_type']}: {min_grade}\n"
                        if reqs[0]['additional_requirements']:
                            response += f"• Additional: {reqs[0]['additional_requirements']}\n"
                    else:
                        response += "Please visit our admission requirements page for detailed information."
                    
                    cursor.close()
                    return {
                        'message': response,
                        'intent': 'admission_requirements',
                        'suggestions': ['Check my eligibility', 'View all requirements', 'Application procedure']
                    }
            
            cursor.close()
            return {
                'message': "I can help you with admission requirements! Please specify which program you're interested in, or visit our Admission Requirements page for detailed information.",
                'intent': 'admission_requirements',
                'suggestions': ['Computer Science', 'Engineering', 'Business', 'View all programs']
            }
            
        except Exception as e:
            return {
                'message': "I can help you with admission requirements. Please visit our Admission Requirements page or specify a program you're interested in.",
                'intent': 'admission_requirements',
                'suggestions': []
            }
    
    def _handle_procedure_query(self, message):
        """Handle application procedure queries"""
        response = """Here's a step-by-step guide to apply:

1. **Check Eligibility**: Use our eligibility checker to see if you meet the requirements
2. **Prepare Documents**: Get your document checklist based on your program and country
3. **Submit Application**: Apply online through our portal or submit offline
4. **Pay Application Fee**: RM 50 application fee
5. **Track Status**: Monitor your application status online

Would you like detailed steps for online or offline application?"""
        
        return {
            'message': response,
            'intent': 'application_procedure',
            'suggestions': ['Online application steps', 'Offline application steps', 'Document checklist']
        }
    
    def _handle_deadline_query(self, message):
        """Handle deadline queries"""
        try:
            cursor = self.conn.cursor(dictionary=True)
            
            cursor.execute("""
                SELECT event_type, start_date, end_date, description, p.program_name
                FROM IMPORTANT_DATE id
                JOIN PROGRAM p ON id.program_id = p.program_id
                WHERE end_date >= CURDATE()
                ORDER BY end_date ASC
                LIMIT 5
            """)
            
            dates = cursor.fetchall()
            cursor.close()
            
            if dates:
                response = "Here are upcoming important dates:\n\n"
                for date in dates:
                    days_left = (date['end_date'] - datetime.now().date()).days if date['end_date'] else None
                    response += f"• {date['event_type']} for {date['program_name']}: "
                    if date['end_date']:
                        response += f"Until {date['end_date'].strftime('%d %B %Y')}"
                        if days_left:
                            response += f" ({days_left} days remaining)"
                    response += "\n"
            else:
                response = "Please check our Important Dates page for the latest deadline information."
            
            return {
                'message': response,
                'intent': 'deadlines',
                'suggestions': ['View all deadlines', 'Set reminder', 'Application periods']
            }
            
        except Exception as e:
            return {
                'message': "Please visit our Important Dates page for deadline information, or contact our admission office.",
                'intent': 'deadlines',
                'suggestions': []
            }
    
    def _handle_document_query(self, message):
        """Handle document checklist queries"""
        response = """I can help you with document requirements! 

The documents you need depend on:
• Your chosen program
• Your country of origin (Malaysia or International)
• Your qualification type

Would you like me to generate a personalized document checklist? Please specify:
1. Which program you're applying for
2. Your country (Malaysia or International)"""
        
        return {
            'message': response,
            'intent': 'documents',
            'suggestions': ['Generate my checklist', 'View sample documents', 'EMGS requirements']
        }
    
    def _handle_fee_query(self, message):
        """Handle fee-related queries"""
        try:
            cursor = self.conn.cursor(dictionary=True)
            
            cursor.execute("""
                SELECT p.program_name, tf.amount, tf.currency, tf.semester
                FROM TUITION_FEE tf
                JOIN PROGRAM p ON tf.program_id = p.program_id
                WHERE tf.academic_year = '2025'
                GROUP BY p.program_id, tf.amount
                LIMIT 3
            """)
            
            fees = cursor.fetchall()
            cursor.close()
            
            if fees:
                response = "Tuition fees vary by program. Here are some examples:\n\n"
                for fee in fees:
                    response += f"• {fee['program_name']}: RM {fee['amount']:.2f} per trimester\n"
                response += "\nVisit our Fees page for complete information, or check scholarship opportunities!"
            else:
                response = "Tuition fees vary by program. Please visit our website or contact us for detailed fee information. We also offer various scholarships and financial aid options!"
            
            return {
                'message': response,
                'intent': 'fees',
                'suggestions': ['View all fees', 'Scholarships', 'Financial aid']
            }
            
        except Exception as e:
            return {
                'message': "For detailed fee information, please visit our website or contact the finance office. We offer various payment plans and scholarships!",
                'intent': 'fees',
                'suggestions': []
            }
    
    def _handle_program_query(self, message):
        """Handle program information queries"""
        response = "SKL University offers programs across multiple faculties including Computer Science, Engineering, Business, Science, Arts, and more. Would you like information about a specific program?"
        
        return {
            'message': response,
            'intent': 'program_info',
            'suggestions': ['Computer Science', 'Engineering', 'Business', 'View all programs']
        }
    
    def _handle_general_query(self, message):
        """Handle general queries"""
        responses = [
            "I'm here to help with admission-related questions! You can ask me about requirements, application procedures, deadlines, documents, fees, or programs.",
            "How can I assist you with your admission inquiry? I can help with requirements, procedures, deadlines, and more!",
            "I can help you with admission requirements, application steps, important dates, document checklists, and program information. What would you like to know?"
        ]
        
        import random
        return {
            'message': random.choice(responses),
            'intent': 'general',
            'suggestions': ['Admission requirements', 'How to apply', 'Important dates', 'Document checklist']
        }
    
    def _save_message(self, session_id, sender_type, message_text, intent):
        """Save message to database"""
        try:
            cursor = self.conn.cursor()
            
            # Get or create session
            cursor.execute("""
                SELECT session_id FROM CHAT_SESSION 
                WHERE session_id = %s LIMIT 1
            """, (session_id,))
            
            session_record = cursor.fetchone()
            
            if not session_record:
                cursor.execute("""
                    INSERT INTO CHAT_SESSION (session_id, start_time, session_status)
                    VALUES (%s, NOW(), 'Active')
                """, (session_id,))
                self.conn.commit()
            
            # Save message
            cursor.execute("""
                INSERT INTO CHAT_MESSAGE 
                (session_id, sender_type, message_text, intent_detected, confidence_score)
                VALUES (%s, %s, %s, %s, %s)
            """, (session_id, sender_type, message_text, intent, 0.80))
            
            self.conn.commit()
            cursor.close()
            
        except Exception as e:
            print(f"Error saving message: {e}")
            # Don't fail the request if message saving fails

