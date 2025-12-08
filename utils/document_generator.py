"""
Document Checklist Generator - Customized based on program, country, and eligibility
"""
from datetime import datetime

class DocumentChecklistGenerator:
    """Generate customized document checklists"""
    
    def __init__(self, db_connection):
        self.conn = db_connection
        
        # Country-specific document requirements
        self.country_documents = {
            'Malaysia': {
                'mandatory': ['Identity Card (MyKad)', 'Birth Certificate'],
                'optional': []
            },
            'International': {
                'mandatory': ['Passport (valid for at least 18 months)', 
                            'Student Visa/EMGS Approval Letter',
                            'Medical Report (from recognized clinic)'],
                'optional': ['English Proficiency Test (IELTS/TOEFL)']
            }
        }
        
        # Program-specific additional documents
        self.program_specific = {
            'Engineering': ['Engineering Drawing Portfolio (if applicable)'],
            'Arts': ['Portfolio of Creative Work'],
            'Medicine': ['Medical Fitness Certificate', 'Criminal Record Check'],
            'Business': ['Business Plan (for Entrepreneurship programs)']
        }
    
    def get_program_info(self, program_id):
        """Get program information"""
        try:
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT p.*, f.faculty_name
                FROM PROGRAM p
                JOIN FACULTY f ON p.faculty_id = f.faculty_id
                WHERE p.program_id = %s
            """, (program_id,))
            
            program = cursor.fetchone()
            cursor.close()
            
            return program
        except Exception as e:
            return None
    
    def generate_checklist(self, program_id, country='Malaysia', eligibility_status='eligible'):
        """Generate customized document checklist"""
        try:
            cursor = self.conn.cursor(dictionary=True)
            
            # Get base documents from database
            cursor.execute("""
                SELECT document_name, is_mandatory, description
                FROM DOCUMENT_CHECKLIST
                WHERE program_id = %s
                ORDER BY is_mandatory DESC, document_name
            """, (program_id,))
            
            base_documents = cursor.fetchall()
            
            # Get program info for program-specific documents
            program_info = self.get_program_info(program_id)
            program_name = program_info['program_name'] if program_info else ''
            faculty_name = program_info['faculty_name'] if program_info else ''
            
            # Build checklist
            checklist = {
                'mandatory': [],
                'optional': [],
                'country_specific': [],
                'program_specific': []
            }
            
            # Add base documents
            for doc in base_documents:
                doc_item = {
                    'name': doc['document_name'],
                    'description': doc['description'],
                    'status': 'pending',
                    'source': 'program_requirement'
                }
                
                if doc['is_mandatory']:
                    checklist['mandatory'].append(doc_item)
                else:
                    checklist['optional'].append(doc_item)
            
            # Add country-specific documents
            is_international = country.lower() not in ['malaysia', 'malaysian']
            country_key = 'International' if is_international else 'Malaysia'
            
            if country_key in self.country_documents:
                for doc_name in self.country_documents[country_key]['mandatory']:
                    checklist['country_specific'].append({
                        'name': doc_name,
                        'description': f'Required for {country_key} applicants',
                        'status': 'pending',
                        'source': 'country_requirement',
                        'mandatory': True
                    })
                
                for doc_name in self.country_documents[country_key]['optional']:
                    checklist['country_specific'].append({
                        'name': doc_name,
                        'description': f'Recommended for {country_key} applicants',
                        'status': 'pending',
                        'source': 'country_requirement',
                        'mandatory': False
                    })
            
            # Add program-specific documents based on program type
            program_lower = program_name.lower()
            for prog_type, docs in self.program_specific.items():
                if prog_type.lower() in program_lower or prog_type.lower() in faculty_name.lower():
                    for doc_name in docs:
                        checklist['program_specific'].append({
                            'name': doc_name,
                            'description': f'Required for {prog_type} programs',
                            'status': 'pending',
                            'source': 'program_specific',
                            'mandatory': True
                        })
            
            # Add EMGS documents for international students
            if is_international:
                checklist['country_specific'].append({
                    'name': 'EMGS Application Form',
                    'description': 'Education Malaysia Global Services application for student visa',
                    'status': 'pending',
                    'source': 'emgs_requirement',
                    'mandatory': True,
                    'link': 'https://educationmalaysia.gov.my/'
                })
            
            # Add UPU documents for Malaysian students (if applicable)
            if not is_international and 'Bachelor' in program_name:
                checklist['optional'].append({
                    'name': 'UPU Application Reference Number',
                    'description': 'If applying through UPU system',
                    'status': 'pending',
                    'source': 'upu_requirement',
                    'mandatory': False
                })
            
            # Add eligibility-based recommendations
            if eligibility_status == 'conditional':
                checklist['optional'].append({
                    'name': 'Additional Supporting Documents',
                    'description': 'Documents to strengthen your application (recommendation letters, certificates, etc.)',
                    'status': 'pending',
                    'source': 'eligibility_recommendation',
                    'mandatory': False
                })
            
            cursor.close()
            
            # Calculate totals
            total_mandatory = len(checklist['mandatory']) + \
                            len([d for d in checklist['country_specific'] if d.get('mandatory', False)]) + \
                            len(checklist['program_specific'])
            
            total_optional = len(checklist['optional']) + \
                           len([d for d in checklist['country_specific'] if not d.get('mandatory', False)])
            
            checklist['summary'] = {
                'total_mandatory': total_mandatory,
                'total_optional': total_optional,
                'total_documents': total_mandatory + total_optional,
                'country': country,
                'program_id': program_id,
                'generated_at': datetime.now().isoformat()
            }
            
            return checklist
            
        except Exception as e:
            return {
                'error': str(e),
                'mandatory': [],
                'optional': [],
                'country_specific': [],
                'program_specific': []
            }


