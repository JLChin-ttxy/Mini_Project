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
                'mandatory': [
                    'Valid Passport (minimum 18 months validity from program start date) - MANDATORY FOR ALL INTERNATIONAL STUDENTS',
                    'Student Visa / EMGS Approval Letter (Education Malaysia Global Services) - MANDATORY FOR ALL INTERNATIONAL STUDENTS',
                    'Medical Examination Report (from recognized clinic/hospital approved by EMGS) - MANDATORY FOR ALL INTERNATIONAL STUDENTS',
                    'English Proficiency Test Results (IELTS/TOEFL/MUET) - Original certificate - MANDATORY',
                    'Financial Proof / Bank Statement (showing minimum RM 30,000 or equivalent for living expenses) - MANDATORY',
                    'Academic Transcripts with Certified English Translation (if original is not in English) - MANDATORY',
                    'Academic Certificates with Certified English Translation (if original is not in English) - MANDATORY',
                    'Passport-sized Photographs (4 copies, white background, 35mm x 50mm) - MANDATORY',
                    'EMGS Application Form (completed and signed) - MANDATORY FOR VISA PROCESSING'
                ],
                'optional': [
                    'Police Clearance Certificate (from home country) - Required for some countries',
                    'No-Objection Certificate (NOC) - if required by home country',
                    'Sponsorship Letter (if sponsored by government or organization)',
                    'Health Insurance Certificate (recommended)',
                    'Character Reference Letter (from previous institution)'
                ]
            }
        }
        
        # Nationality-specific identity documents
        self.nationality_documents = {
            'Indonesia': {
                'identity': 'KTP (Kartu Tanda Penduduk) or Passport',
                'additional': ['Academic transcripts with certified English translation']
            },
            'China': {
                'identity': 'Chinese ID Card or Passport',
                'additional': ['Notarized academic certificates', 'HSK certificate (if applicable)']
            },
            'India': {
                'identity': 'Aadhaar Card or Passport',
                'additional': ['Academic transcripts with certified English translation']
            },
            'Bangladesh': {
                'identity': 'National ID Card or Passport',
                'additional': ['Academic transcripts with certified English translation']
            },
            'Thailand': {
                'identity': 'Thai National ID Card or Passport',
                'additional': ['Academic transcripts with certified English translation']
            },
            'Vietnam': {
                'identity': 'Vietnamese ID Card or Passport',
                'additional': ['Academic transcripts with certified English translation']
            },
            'Philippines': {
                'identity': 'Philippine National ID or Passport',
                'additional': ['Academic transcripts with certified English translation']
            },
            'Pakistan': {
                'identity': 'CNIC (Computerized National Identity Card) or Passport',
                'additional': ['Academic transcripts with certified English translation']
            },
            'Nepal': {
                'identity': 'Nepali Citizenship Certificate or Passport',
                'additional': ['Academic transcripts with certified English translation']
            },
            'Sri Lanka': {
                'identity': 'National Identity Card or Passport',
                'additional': ['Academic transcripts with certified English translation']
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
                # For international students, replace base mandatory documents with international-specific ones
                if is_international:
                    # Clear Malaysian-specific mandatory documents
                    checklist['mandatory'] = []
                    # Add international mandatory documents
                    for doc_name in self.country_documents[country_key]['mandatory']:
                        checklist['mandatory'].append({
                            'name': doc_name,
                            'description': f'MANDATORY for international students - Required for visa processing',
                            'status': 'pending',
                            'source': 'international_requirement',
                            'mandatory': True
                        })
                else:
                    # For Malaysian students, add country-specific documents
                    for doc_name in self.country_documents[country_key]['mandatory']:
                        checklist['country_specific'].append({
                            'name': doc_name,
                            'description': f'Required for {country_key} applicants',
                            'status': 'pending',
                            'source': 'country_requirement',
                            'mandatory': True
                        })
                
                # Add optional documents
                for doc_name in self.country_documents[country_key]['optional']:
                    checklist['country_specific'].append({
                        'name': doc_name,
                        'description': f'Recommended for {country_key} applicants',
                        'status': 'pending',
                        'source': 'country_requirement',
                        'mandatory': False
                    })
            
            # Add nationality-specific identity documents for international students
            if is_international:
                # Check if we have specific nationality requirements
                nationality = country.strip()
                if nationality in self.nationality_documents:
                    nat_docs = self.nationality_documents[nationality]
                    checklist['country_specific'].append({
                        'name': f'National ID Document ({nat_docs["identity"]})',
                        'description': f'Required identity document for {nationality} nationals',
                        'status': 'pending',
                        'source': 'nationality_requirement',
                        'mandatory': True
                    })
                    
                    for additional_doc in nat_docs.get('additional', []):
                        checklist['country_specific'].append({
                            'name': additional_doc,
                            'description': f'Additional requirement for {nationality} applicants',
                            'status': 'pending',
                            'source': 'nationality_requirement',
                            'mandatory': True
                        })
                else:
                    # Generic international requirement
                    checklist['country_specific'].append({
                        'name': 'National ID Document or Passport',
                        'description': 'Valid national identity document from your country',
                        'status': 'pending',
                        'source': 'nationality_requirement',
                        'mandatory': True
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


