"""
Script to add Postgraduate Programs (Master and PhD) to the database
Run this script to populate the database with postgraduate programs
"""
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.db_helper import get_db_connection

def add_postgraduate_programs():
    """Add Master's and PhD programs to the database"""
    conn = get_db_connection()
    if not conn:
        print("Error: Could not connect to database")
        return False
    
    try:
        cursor = conn.cursor()
        
        # Master's Programs
        master_programs = [
            (1, 'Master of Business Administration (MBA)', 'Master', 2, 'Senior Manager, Business Consultant, Executive Director, Strategic Planner', 'Comprehensive MBA program covering strategic management, leadership, finance, marketing, and operations. Designed for working professionals.'),
            (1, 'Master of Accounting', 'Master', 1.5, 'Senior Accountant, Financial Controller, Audit Manager, Tax Consultant', 'Advanced accounting program focusing on financial reporting, auditing, taxation, and corporate governance. Prepares for professional accounting qualifications.'),
            (2, 'Master of Arts in Psychology', 'Master', 2, 'Clinical Psychologist, Research Psychologist, Counsellor, Organizational Psychologist', 'Advanced psychology program with specialization in clinical, organizational, or research psychology. Includes thesis component.'),
            (2, 'Master of Communication', 'Master', 1.5, 'Communication Manager, PR Director, Media Strategist, Corporate Communications Head', 'Strategic communication program covering media relations, digital communication, crisis management, and communication research.'),
            (3, 'Master of Economics', 'Master', 2, 'Economic Analyst, Policy Advisor, Research Economist, Financial Economist', 'Advanced economics program with focus on econometrics, economic policy, and financial economics. Includes research thesis.'),
            (3, 'Master of Marketing', 'Master', 1.5, 'Marketing Director, Brand Manager, Digital Marketing Head, Market Research Director', 'Strategic marketing program covering consumer behavior, brand management, digital marketing, and marketing analytics.'),
            (4, 'Master of Computer Science', 'Master', 2, 'Senior Software Engineer, Research Scientist, AI Specialist, Systems Architect', 'Advanced computing program with specialization in AI, data science, cybersecurity, or software engineering. Research-based program.'),
            (4, 'Master of Information Technology', 'Master', 1.5, 'IT Manager, Technology Consultant, Systems Manager, IT Project Director', 'IT management program focusing on enterprise systems, IT strategy, project management, and emerging technologies.'),
            (5, 'Master of Science in Actuarial Science', 'Master', 2, 'Senior Actuary, Risk Manager, Insurance Analyst, Financial Modeler', 'Advanced actuarial program preparing for professional actuarial examinations. Covers advanced risk modeling and financial mathematics.'),
            (5, 'Master of Science in Biotechnology', 'Master', 2, 'Research Scientist, Biotechnologist, R&D Manager, Quality Control Director', 'Research-focused biotechnology program covering genetic engineering, bioprocessing, and biopharmaceuticals.'),
            (6, 'Master of Engineering (Civil Engineering)', 'Master', 2, 'Senior Civil Engineer, Project Director, Structural Consultant, Engineering Manager', 'Advanced civil engineering program with specialization in structural engineering, geotechnical engineering, or construction management.'),
            (6, 'Master of Engineering (Electrical Engineering)', 'Master', 2, 'Senior Electrical Engineer, Power Systems Manager, Automation Director, Research Engineer', 'Advanced electrical engineering program focusing on power systems, renewable energy, or control systems.'),
        ]
        
        # PhD Programs
        phd_programs = [
            (1, 'Doctor of Philosophy (PhD) in Accounting', 'PhD', 3, 'Professor, Research Director, Senior Consultant, Policy Advisor', 'Research-based PhD program in accounting. Students conduct original research in financial accounting, management accounting, auditing, or taxation.'),
            (1, 'Doctor of Philosophy (PhD) in Business Administration', 'PhD', 3, 'Professor, Business Research Director, Strategic Advisor, Academic Researcher', 'Doctoral program in business administration. Focus on advanced research in management, strategy, finance, or organizational behavior.'),
            (2, 'Doctor of Philosophy (PhD) in Psychology', 'PhD', 3, 'Professor, Clinical Research Director, Senior Psychologist, Academic Researcher', 'Research-focused PhD program in psychology. Specialization in clinical, social, cognitive, or organizational psychology.'),
            (2, 'Doctor of Philosophy (PhD) in Communication', 'PhD', 3, 'Professor, Communication Research Director, Media Analyst, Academic Researcher', 'Doctoral program in communication studies. Advanced research in media, public relations, or digital communication.'),
            (3, 'Doctor of Philosophy (PhD) in Economics', 'PhD', 3, 'Professor, Economic Research Director, Policy Advisor, Academic Researcher', 'Research-based PhD program in economics. Advanced econometric analysis, economic theory, and policy research.'),
            (3, 'Doctor of Philosophy (PhD) in Marketing', 'PhD', 3, 'Professor, Marketing Research Director, Brand Strategist, Academic Researcher', 'Doctoral program in marketing. Original research in consumer behavior, brand management, or digital marketing.'),
            (4, 'Doctor of Philosophy (PhD) in Computer Science', 'PhD', 3, 'Professor, Research Director, Senior Research Scientist, Technology Innovator', 'Research-focused PhD program in computer science. Specialization in AI, data science, cybersecurity, or software engineering.'),
            (4, 'Doctor of Philosophy (PhD) in Information Technology', 'PhD', 3, 'Professor, IT Research Director, Technology Consultant, Academic Researcher', 'Doctoral program in information technology. Advanced research in enterprise systems, IT management, or emerging technologies.'),
            (5, 'Doctor of Philosophy (PhD) in Actuarial Science', 'PhD', 3, 'Professor, Senior Actuary, Research Director, Academic Researcher', 'Research-based PhD program in actuarial science. Advanced risk modeling, financial mathematics, and insurance research.'),
            (5, 'Doctor of Philosophy (PhD) in Biotechnology', 'PhD', 3, 'Professor, Research Director, Senior Biotechnologist, Academic Researcher', 'Doctoral program in biotechnology. Original research in genetic engineering, bioprocessing, or biopharmaceuticals.'),
            (6, 'Doctor of Philosophy (PhD) in Civil Engineering', 'PhD', 3, 'Professor, Senior Research Engineer, Engineering Consultant, Academic Researcher', 'Research-focused PhD program in civil engineering. Advanced research in structural engineering, geotechnical engineering, or construction materials.'),
            (6, 'Doctor of Philosophy (PhD) in Electrical Engineering', 'PhD', 3, 'Professor, Senior Research Engineer, Technology Innovator, Academic Researcher', 'Doctoral program in electrical engineering. Original research in power systems, renewable energy, or control systems.'),
        ]
        
        print("Adding Master's programs...")
        master_ids = {}
        for faculty_id, program_name, level, duration, career, description in master_programs:
            # Check if program already exists
            cursor.execute("""
                SELECT program_id FROM PROGRAM 
                WHERE program_name = %s AND level = %s
            """, (program_name, level))
            existing = cursor.fetchone()
            
            if existing:
                print(f"  - {program_name} already exists (ID: {existing[0]})")
                master_ids[program_name] = existing[0]
            else:
                cursor.execute("""
                    INSERT INTO PROGRAM (faculty_id, program_name, level, duration_years, career_prospects, description)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (faculty_id, program_name, level, duration, career, description))
                program_id = cursor.lastrowid
                master_ids[program_name] = program_id
                print(f"  + Added {program_name} (ID: {program_id})")
        
        print("\nAdding PhD programs...")
        phd_ids = {}
        for faculty_id, program_name, level, duration, career, description in phd_programs:
            # Check if program already exists
            cursor.execute("""
                SELECT program_id FROM PROGRAM 
                WHERE program_name = %s AND level = %s
            """, (program_name, level))
            existing = cursor.fetchone()
            
            if existing:
                print(f"  - {program_name} already exists (ID: {existing[0]})")
                phd_ids[program_name] = existing[0]
            else:
                cursor.execute("""
                    INSERT INTO PROGRAM (faculty_id, program_name, level, duration_years, career_prospects, description)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (faculty_id, program_name, level, duration, career, description))
                program_id = cursor.lastrowid
                phd_ids[program_name] = program_id
                print(f"  + Added {program_name} (ID: {program_id})")
        
        # Add admission requirements for Master's programs
        print("\nAdding admission requirements for Master's programs...")
        master_requirements = {
            'Master of Business Administration (MBA)': [
                ('Bachelor', 'Minimum CGPA 2.75', 'Bachelor degree in any field. Minimum 2 years work experience preferred.', 'Interview may be required'),
                ('Professional Qualification', 'Recognized by MQA', 'With relevant work experience', None),
            ],
            'Master of Accounting': [
                ('Bachelor', 'Minimum CGPA 2.75', 'Bachelor degree in Accounting or related field', None),
            ],
            'Master of Arts in Psychology': [
                ('Bachelor', 'Minimum CGPA 2.75', 'Bachelor degree in Psychology or related field', 'Interview required'),
            ],
            'Master of Communication': [
                ('Bachelor', 'Minimum CGPA 2.75', 'Bachelor degree in Communication, Media, or related field', None),
            ],
            'Master of Economics': [
                ('Bachelor', 'Minimum CGPA 2.75', 'Bachelor degree in Economics or related field with strong quantitative background', None),
            ],
            'Master of Marketing': [
                ('Bachelor', 'Minimum CGPA 2.75', 'Bachelor degree in Marketing, Business, or related field', None),
            ],
            'Master of Computer Science': [
                ('Bachelor', 'Minimum CGPA 2.75', 'Bachelor degree in Computer Science, IT, or related field', 'Research proposal required'),
            ],
            'Master of Information Technology': [
                ('Bachelor', 'Minimum CGPA 2.75', 'Bachelor degree in IT, Computer Science, or related field', None),
            ],
            'Master of Science in Actuarial Science': [
                ('Bachelor', 'Minimum CGPA 2.75', 'Bachelor degree in Actuarial Science, Mathematics, or Statistics', None),
            ],
            'Master of Science in Biotechnology': [
                ('Bachelor', 'Minimum CGPA 2.75', 'Bachelor degree in Biotechnology, Biology, or related field', 'Research proposal required'),
            ],
            'Master of Engineering (Civil Engineering)': [
                ('Bachelor', 'Minimum CGPA 2.75', 'Bachelor degree in Civil Engineering or related field. BEM registration preferred.', 'Research proposal required'),
            ],
            'Master of Engineering (Electrical Engineering)': [
                ('Bachelor', 'Minimum CGPA 2.75', 'Bachelor degree in Electrical Engineering or related field. BEM registration preferred.', 'Research proposal required'),
            ],
        }
        
        for program_name, requirements in master_requirements.items():
            if program_name in master_ids:
                program_id = master_ids[program_name]
                for qual_type, min_grade, additional, exam_info in requirements:
                    # Check if requirement already exists
                    cursor.execute("""
                        SELECT requirement_id FROM ADMISSION_REQUIREMENT
                        WHERE program_id = %s AND qualification_type = %s
                    """, (program_id, qual_type))
                    if not cursor.fetchone():
                        cursor.execute("""
                            INSERT INTO ADMISSION_REQUIREMENT 
                            (program_id, qualification_type, minimum_grade, additional_requirements, entrance_exam_info)
                            VALUES (%s, %s, %s, %s, %s)
                        """, (program_id, qual_type, min_grade, additional, exam_info))
                        print(f"    + Added requirement: {qual_type} for {program_name}")
        
        # Add admission requirements for PhD programs
        print("\nAdding admission requirements for PhD programs...")
        phd_requirements = {
            'Doctor of Philosophy (PhD) in Accounting': [
                ('Master', 'Minimum CGPA 3.00', 'Master degree in Accounting or related field', 'Research proposal and supervisor acceptance required'),
                ('Bachelor', 'Minimum CGPA 3.67', 'First Class Honours Bachelor degree in Accounting or related field', 'Research proposal and supervisor acceptance required'),
            ],
            'Doctor of Philosophy (PhD) in Business Administration': [
                ('Master', 'Minimum CGPA 3.00', 'Master degree in Business Administration or related field', 'Research proposal and supervisor acceptance required'),
                ('Bachelor', 'Minimum CGPA 3.67', 'First Class Honours Bachelor degree in Business or related field', 'Research proposal and supervisor acceptance required'),
            ],
            'Doctor of Philosophy (PhD) in Psychology': [
                ('Master', 'Minimum CGPA 3.00', 'Master degree in Psychology or related field', 'Research proposal and supervisor acceptance required'),
            ],
            'Doctor of Philosophy (PhD) in Communication': [
                ('Master', 'Minimum CGPA 3.00', 'Master degree in Communication, Media, or related field', 'Research proposal and supervisor acceptance required'),
            ],
            'Doctor of Philosophy (PhD) in Economics': [
                ('Master', 'Minimum CGPA 3.00', 'Master degree in Economics or related field with strong quantitative background', 'Research proposal and supervisor acceptance required'),
            ],
            'Doctor of Philosophy (PhD) in Marketing': [
                ('Master', 'Minimum CGPA 3.00', 'Master degree in Marketing, Business, or related field', 'Research proposal and supervisor acceptance required'),
            ],
            'Doctor of Philosophy (PhD) in Computer Science': [
                ('Master', 'Minimum CGPA 3.00', 'Master degree in Computer Science, IT, or related field', 'Research proposal and supervisor acceptance required'),
                ('Bachelor', 'Minimum CGPA 3.67', 'First Class Honours Bachelor degree in Computer Science or related field', 'Research proposal and supervisor acceptance required'),
            ],
            'Doctor of Philosophy (PhD) in Information Technology': [
                ('Master', 'Minimum CGPA 3.00', 'Master degree in IT, Computer Science, or related field', 'Research proposal and supervisor acceptance required'),
            ],
            'Doctor of Philosophy (PhD) in Actuarial Science': [
                ('Master', 'Minimum CGPA 3.00', 'Master degree in Actuarial Science, Mathematics, or Statistics', 'Research proposal and supervisor acceptance required'),
            ],
            'Doctor of Philosophy (PhD) in Biotechnology': [
                ('Master', 'Minimum CGPA 3.00', 'Master degree in Biotechnology, Biology, or related field', 'Research proposal and supervisor acceptance required'),
            ],
            'Doctor of Philosophy (PhD) in Civil Engineering': [
                ('Master', 'Minimum CGPA 3.00', 'Master degree in Civil Engineering or related field. BEM registration preferred.', 'Research proposal and supervisor acceptance required'),
                ('Bachelor', 'Minimum CGPA 3.67', 'First Class Honours Bachelor degree in Civil Engineering', 'Research proposal and supervisor acceptance required'),
            ],
            'Doctor of Philosophy (PhD) in Electrical Engineering': [
                ('Master', 'Minimum CGPA 3.00', 'Master degree in Electrical Engineering or related field. BEM registration preferred.', 'Research proposal and supervisor acceptance required'),
                ('Bachelor', 'Minimum CGPA 3.67', 'First Class Honours Bachelor degree in Electrical Engineering', 'Research proposal and supervisor acceptance required'),
            ],
        }
        
        for program_name, requirements in phd_requirements.items():
            if program_name in phd_ids:
                program_id = phd_ids[program_name]
                for qual_type, min_grade, additional, exam_info in requirements:
                    # Check if requirement already exists
                    cursor.execute("""
                        SELECT requirement_id FROM ADMISSION_REQUIREMENT
                        WHERE program_id = %s AND qualification_type = %s
                    """, (program_id, qual_type))
                    if not cursor.fetchone():
                        cursor.execute("""
                            INSERT INTO ADMISSION_REQUIREMENT 
                            (program_id, qualification_type, minimum_grade, additional_requirements, entrance_exam_info)
                            VALUES (%s, %s, %s, %s, %s)
                        """, (program_id, qual_type, min_grade, additional, exam_info))
                        print(f"    + Added requirement: {qual_type} for {program_name}")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("\n" + "="*60)
        print("SUCCESS! Postgraduate programs have been added to the database.")
        print("="*60)
        print(f"\nTotal Master's programs: {len(master_ids)}")
        print(f"Total PhD programs: {len(phd_ids)}")
        print("\nYou can now refresh the requirements page to see the programs.")
        
        return True
        
    except Exception as e:
        print(f"\nError: {str(e)}")
        if conn:
            conn.rollback()
            conn.close()
        return False

if __name__ == "__main__":
    print("="*60)
    print("Adding Postgraduate Programs to Database")
    print("="*60)
    print()
    add_postgraduate_programs()
