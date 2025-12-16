-- Add Postgraduate Programs (Master and PhD) to the database
-- Following UTAR style and structure

USE university_admission_db;

-- ============================================================================
-- MASTER'S PROGRAMS
-- ============================================================================

-- Faculty of Accountancy and Management (Faculty ID: 1)
INSERT INTO PROGRAM (faculty_id, program_name, level, duration_years, career_prospects, description) VALUES
(1, 'Master of Business Administration (MBA)', 'Master', 2, 'Senior Manager, Business Consultant, Executive Director, Strategic Planner', 'Comprehensive MBA program covering strategic management, leadership, finance, marketing, and operations. Designed for working professionals.'),
(1, 'Master of Accounting', 'Master', 1.5, 'Senior Accountant, Financial Controller, Audit Manager, Tax Consultant', 'Advanced accounting program focusing on financial reporting, auditing, taxation, and corporate governance. Prepares for professional accounting qualifications.'),

-- Faculty of Arts and Social Science (Faculty ID: 2)
(2, 'Master of Arts in Psychology', 'Master', 2, 'Clinical Psychologist, Research Psychologist, Counsellor, Organizational Psychologist', 'Advanced psychology program with specialization in clinical, organizational, or research psychology. Includes thesis component.'),
(2, 'Master of Communication', 'Master', 1.5, 'Communication Manager, PR Director, Media Strategist, Corporate Communications Head', 'Strategic communication program covering media relations, digital communication, crisis management, and communication research.'),

-- Faculty of Business and Finance (Faculty ID: 3)
(3, 'Master of Economics', 'Master', 2, 'Economic Analyst, Policy Advisor, Research Economist, Financial Economist', 'Advanced economics program with focus on econometrics, economic policy, and financial economics. Includes research thesis.'),
(3, 'Master of Marketing', 'Master', 1.5, 'Marketing Director, Brand Manager, Digital Marketing Head, Market Research Director', 'Strategic marketing program covering consumer behavior, brand management, digital marketing, and marketing analytics.'),

-- Faculty of Information and Communication Technology (Faculty ID: 4)
(4, 'Master of Computer Science', 'Master', 2, 'Senior Software Engineer, Research Scientist, AI Specialist, Systems Architect', 'Advanced computing program with specialization in AI, data science, cybersecurity, or software engineering. Research-based program.'),
(4, 'Master of Information Technology', 'Master', 1.5, 'IT Manager, Technology Consultant, Systems Manager, IT Project Director', 'IT management program focusing on enterprise systems, IT strategy, project management, and emerging technologies.'),

-- Faculty of Science (Faculty ID: 5)
(5, 'Master of Science in Actuarial Science', 'Master', 2, 'Senior Actuary, Risk Manager, Insurance Analyst, Financial Modeler', 'Advanced actuarial program preparing for professional actuarial examinations. Covers advanced risk modeling and financial mathematics.'),
(5, 'Master of Science in Biotechnology', 'Master', 2, 'Research Scientist, Biotechnologist, R&D Manager, Quality Control Director', 'Research-focused biotechnology program covering genetic engineering, bioprocessing, and biopharmaceuticals.'),

-- Faculty of Engineering and Green Technology (Faculty ID: 6)
(6, 'Master of Engineering (Civil Engineering)', 'Master', 2, 'Senior Civil Engineer, Project Director, Structural Consultant, Engineering Manager', 'Advanced civil engineering program with specialization in structural engineering, geotechnical engineering, or construction management.'),
(6, 'Master of Engineering (Electrical Engineering)', 'Master', 2, 'Senior Electrical Engineer, Power Systems Manager, Automation Director, Research Engineer', 'Advanced electrical engineering program focusing on power systems, renewable energy, or control systems.');

-- ============================================================================
-- PhD PROGRAMS
-- ============================================================================

-- Faculty of Accountancy and Management (Faculty ID: 1)
INSERT INTO PROGRAM (faculty_id, program_name, level, duration_years, career_prospects, description) VALUES
(1, 'Doctor of Philosophy (PhD) in Accounting', 'PhD', 3, 'Professor, Research Director, Senior Consultant, Policy Advisor', 'Research-based PhD program in accounting. Students conduct original research in financial accounting, management accounting, auditing, or taxation.'),
(1, 'Doctor of Philosophy (PhD) in Business Administration', 'PhD', 3, 'Professor, Business Research Director, Strategic Advisor, Academic Researcher', 'Doctoral program in business administration. Focus on advanced research in management, strategy, finance, or organizational behavior.'),

-- Faculty of Arts and Social Science (Faculty ID: 2)
(2, 'Doctor of Philosophy (PhD) in Psychology', 'PhD', 3, 'Professor, Clinical Research Director, Senior Psychologist, Academic Researcher', 'Research-focused PhD program in psychology. Specialization in clinical, social, cognitive, or organizational psychology.'),
(2, 'Doctor of Philosophy (PhD) in Communication', 'PhD', 3, 'Professor, Communication Research Director, Media Analyst, Academic Researcher', 'Doctoral program in communication studies. Advanced research in media, public relations, or digital communication.'),

-- Faculty of Business and Finance (Faculty ID: 3)
(3, 'Doctor of Philosophy (PhD) in Economics', 'PhD', 3, 'Professor, Economic Research Director, Policy Advisor, Academic Researcher', 'Research-based PhD program in economics. Advanced econometric analysis, economic theory, and policy research.'),
(3, 'Doctor of Philosophy (PhD) in Marketing', 'PhD', 3, 'Professor, Marketing Research Director, Brand Strategist, Academic Researcher', 'Doctoral program in marketing. Original research in consumer behavior, brand management, or digital marketing.'),

-- Faculty of Information and Communication Technology (Faculty ID: 4)
(4, 'Doctor of Philosophy (PhD) in Computer Science', 'PhD', 3, 'Professor, Research Director, Senior Research Scientist, Technology Innovator', 'Research-focused PhD program in computer science. Specialization in AI, data science, cybersecurity, or software engineering.'),
(4, 'Doctor of Philosophy (PhD) in Information Technology', 'PhD', 3, 'Professor, IT Research Director, Technology Consultant, Academic Researcher', 'Doctoral program in information technology. Advanced research in enterprise systems, IT management, or emerging technologies.'),

-- Faculty of Science (Faculty ID: 5)
(5, 'Doctor of Philosophy (PhD) in Actuarial Science', 'PhD', 3, 'Professor, Senior Actuary, Research Director, Academic Researcher', 'Research-based PhD program in actuarial science. Advanced risk modeling, financial mathematics, and insurance research.'),
(5, 'Doctor of Philosophy (PhD) in Biotechnology', 'PhD', 3, 'Professor, Research Director, Senior Biotechnologist, Academic Researcher', 'Doctoral program in biotechnology. Original research in genetic engineering, bioprocessing, or biopharmaceuticals.'),

-- Faculty of Engineering and Green Technology (Faculty ID: 6)
(6, 'Doctor of Philosophy (PhD) in Civil Engineering', 'PhD', 3, 'Professor, Senior Research Engineer, Engineering Consultant, Academic Researcher', 'Research-focused PhD program in civil engineering. Advanced research in structural engineering, geotechnical engineering, or construction materials.'),
(6, 'Doctor of Philosophy (PhD) in Electrical Engineering', 'PhD', 3, 'Professor, Senior Research Engineer, Technology Innovator, Academic Researcher', 'Doctoral program in electrical engineering. Original research in power systems, renewable energy, or control systems.');

-- ============================================================================
-- ADMISSION REQUIREMENTS FOR MASTER'S PROGRAMS
-- ============================================================================

-- Get the program IDs for Master's programs (assuming they were just inserted)
-- We'll use subqueries to get the program IDs

-- Master of Business Administration (MBA)
INSERT INTO ADMISSION_REQUIREMENT (program_id, qualification_type, minimum_grade, additional_requirements, entrance_exam_info)
SELECT program_id, 'Bachelor', 'Minimum CGPA 2.75', 'Bachelor degree in any field. Minimum 2 years work experience preferred.', 'Interview may be required'
FROM PROGRAM WHERE program_name = 'Master of Business Administration (MBA)' AND level = 'Master';

INSERT INTO ADMISSION_REQUIREMENT (program_id, qualification_type, minimum_grade, additional_requirements, entrance_exam_info)
SELECT program_id, 'Professional Qualification', 'Recognized by MQA', 'With relevant work experience', NULL
FROM PROGRAM WHERE program_name = 'Master of Business Administration (MBA)' AND level = 'Master';

-- Master of Accounting
INSERT INTO ADMISSION_REQUIREMENT (program_id, qualification_type, minimum_grade, additional_requirements, entrance_exam_info)
SELECT program_id, 'Bachelor', 'Minimum CGPA 2.75', 'Bachelor degree in Accounting or related field', NULL
FROM PROGRAM WHERE program_name = 'Master of Accounting' AND level = 'Master';

-- Master of Arts in Psychology
INSERT INTO ADMISSION_REQUIREMENT (program_id, qualification_type, minimum_grade, additional_requirements, entrance_exam_info)
SELECT program_id, 'Bachelor', 'Minimum CGPA 2.75', 'Bachelor degree in Psychology or related field', 'Interview required'
FROM PROGRAM WHERE program_name = 'Master of Arts in Psychology' AND level = 'Master';

-- Master of Communication
INSERT INTO ADMISSION_REQUIREMENT (program_id, qualification_type, minimum_grade, additional_requirements, entrance_exam_info)
SELECT program_id, 'Bachelor', 'Minimum CGPA 2.75', 'Bachelor degree in Communication, Media, or related field', NULL
FROM PROGRAM WHERE program_name = 'Master of Communication' AND level = 'Master';

-- Master of Economics
INSERT INTO ADMISSION_REQUIREMENT (program_id, qualification_type, minimum_grade, additional_requirements, entrance_exam_info)
SELECT program_id, 'Bachelor', 'Minimum CGPA 2.75', 'Bachelor degree in Economics or related field with strong quantitative background', NULL
FROM PROGRAM WHERE program_name = 'Master of Economics' AND level = 'Master';

-- Master of Marketing
INSERT INTO ADMISSION_REQUIREMENT (program_id, qualification_type, minimum_grade, additional_requirements, entrance_exam_info)
SELECT program_id, 'Bachelor', 'Minimum CGPA 2.75', 'Bachelor degree in Marketing, Business, or related field', NULL
FROM PROGRAM WHERE program_name = 'Master of Marketing' AND level = 'Master';

-- Master of Computer Science
INSERT INTO ADMISSION_REQUIREMENT (program_id, qualification_type, minimum_grade, additional_requirements, entrance_exam_info)
SELECT program_id, 'Bachelor', 'Minimum CGPA 2.75', 'Bachelor degree in Computer Science, IT, or related field', 'Research proposal required'
FROM PROGRAM WHERE program_name = 'Master of Computer Science' AND level = 'Master';

-- Master of Information Technology
INSERT INTO ADMISSION_REQUIREMENT (program_id, qualification_type, minimum_grade, additional_requirements, entrance_exam_info)
SELECT program_id, 'Bachelor', 'Minimum CGPA 2.75', 'Bachelor degree in IT, Computer Science, or related field', NULL
FROM PROGRAM WHERE program_name = 'Master of Information Technology' AND level = 'Master';

-- Master of Science in Actuarial Science
INSERT INTO ADMISSION_REQUIREMENT (program_id, qualification_type, minimum_grade, additional_requirements, entrance_exam_info)
SELECT program_id, 'Bachelor', 'Minimum CGPA 2.75', 'Bachelor degree in Actuarial Science, Mathematics, or Statistics', NULL
FROM PROGRAM WHERE program_name = 'Master of Science in Actuarial Science' AND level = 'Master';

-- Master of Science in Biotechnology
INSERT INTO ADMISSION_REQUIREMENT (program_id, qualification_type, minimum_grade, additional_requirements, entrance_exam_info)
SELECT program_id, 'Bachelor', 'Minimum CGPA 2.75', 'Bachelor degree in Biotechnology, Biology, or related field', 'Research proposal required'
FROM PROGRAM WHERE program_name = 'Master of Science in Biotechnology' AND level = 'Master';

-- Master of Engineering (Civil Engineering)
INSERT INTO ADMISSION_REQUIREMENT (program_id, qualification_type, minimum_grade, additional_requirements, entrance_exam_info)
SELECT program_id, 'Bachelor', 'Minimum CGPA 2.75', 'Bachelor degree in Civil Engineering or related field. BEM registration preferred.', 'Research proposal required'
FROM PROGRAM WHERE program_name = 'Master of Engineering (Civil Engineering)' AND level = 'Master';

-- Master of Engineering (Electrical Engineering)
INSERT INTO ADMISSION_REQUIREMENT (program_id, qualification_type, minimum_grade, additional_requirements, entrance_exam_info)
SELECT program_id, 'Bachelor', 'Minimum CGPA 2.75', 'Bachelor degree in Electrical Engineering or related field. BEM registration preferred.', 'Research proposal required'
FROM PROGRAM WHERE program_name = 'Master of Engineering (Electrical Engineering)' AND level = 'Master';

-- ============================================================================
-- ADMISSION REQUIREMENTS FOR PhD PROGRAMS
-- ============================================================================

-- Doctor of Philosophy (PhD) in Accounting
INSERT INTO ADMISSION_REQUIREMENT (program_id, qualification_type, minimum_grade, additional_requirements, entrance_exam_info)
SELECT program_id, 'Master', 'Minimum CGPA 3.00', 'Master degree in Accounting or related field', 'Research proposal and supervisor acceptance required'
FROM PROGRAM WHERE program_name = 'Doctor of Philosophy (PhD) in Accounting' AND level = 'PhD';

INSERT INTO ADMISSION_REQUIREMENT (program_id, qualification_type, minimum_grade, additional_requirements, entrance_exam_info)
SELECT program_id, 'Bachelor', 'Minimum CGPA 3.67', 'First Class Honours Bachelor degree in Accounting or related field', 'Research proposal and supervisor acceptance required'
FROM PROGRAM WHERE program_name = 'Doctor of Philosophy (PhD) in Accounting' AND level = 'PhD';

-- Doctor of Philosophy (PhD) in Business Administration
INSERT INTO ADMISSION_REQUIREMENT (program_id, qualification_type, minimum_grade, additional_requirements, entrance_exam_info)
SELECT program_id, 'Master', 'Minimum CGPA 3.00', 'Master degree in Business Administration or related field', 'Research proposal and supervisor acceptance required'
FROM PROGRAM WHERE program_name = 'Doctor of Philosophy (PhD) in Business Administration' AND level = 'PhD';

INSERT INTO ADMISSION_REQUIREMENT (program_id, qualification_type, minimum_grade, additional_requirements, entrance_exam_info)
SELECT program_id, 'Bachelor', 'Minimum CGPA 3.67', 'First Class Honours Bachelor degree in Business or related field', 'Research proposal and supervisor acceptance required'
FROM PROGRAM WHERE program_name = 'Doctor of Philosophy (PhD) in Business Administration' AND level = 'PhD';

-- Doctor of Philosophy (PhD) in Psychology
INSERT INTO ADMISSION_REQUIREMENT (program_id, qualification_type, minimum_grade, additional_requirements, entrance_exam_info)
SELECT program_id, 'Master', 'Minimum CGPA 3.00', 'Master degree in Psychology or related field', 'Research proposal and supervisor acceptance required'
FROM PROGRAM WHERE program_name = 'Doctor of Philosophy (PhD) in Psychology' AND level = 'PhD';

-- Doctor of Philosophy (PhD) in Communication
INSERT INTO ADMISSION_REQUIREMENT (program_id, qualification_type, minimum_grade, additional_requirements, entrance_exam_info)
SELECT program_id, 'Master', 'Minimum CGPA 3.00', 'Master degree in Communication, Media, or related field', 'Research proposal and supervisor acceptance required'
FROM PROGRAM WHERE program_name = 'Doctor of Philosophy (PhD) in Communication' AND level = 'PhD';

-- Doctor of Philosophy (PhD) in Economics
INSERT INTO ADMISSION_REQUIREMENT (program_id, qualification_type, minimum_grade, additional_requirements, entrance_exam_info)
SELECT program_id, 'Master', 'Minimum CGPA 3.00', 'Master degree in Economics or related field with strong quantitative background', 'Research proposal and supervisor acceptance required'
FROM PROGRAM WHERE program_name = 'Doctor of Philosophy (PhD) in Economics' AND level = 'PhD';

-- Doctor of Philosophy (PhD) in Marketing
INSERT INTO ADMISSION_REQUIREMENT (program_id, qualification_type, minimum_grade, additional_requirements, entrance_exam_info)
SELECT program_id, 'Master', 'Minimum CGPA 3.00', 'Master degree in Marketing, Business, or related field', 'Research proposal and supervisor acceptance required'
FROM PROGRAM WHERE program_name = 'Doctor of Philosophy (PhD) in Marketing' AND level = 'PhD';

-- Doctor of Philosophy (PhD) in Computer Science
INSERT INTO ADMISSION_REQUIREMENT (program_id, qualification_type, minimum_grade, additional_requirements, entrance_exam_info)
SELECT program_id, 'Master', 'Minimum CGPA 3.00', 'Master degree in Computer Science, IT, or related field', 'Research proposal and supervisor acceptance required'
FROM PROGRAM WHERE program_name = 'Doctor of Philosophy (PhD) in Computer Science' AND level = 'PhD';

INSERT INTO ADMISSION_REQUIREMENT (program_id, qualification_type, minimum_grade, additional_requirements, entrance_exam_info)
SELECT program_id, 'Bachelor', 'Minimum CGPA 3.67', 'First Class Honours Bachelor degree in Computer Science or related field', 'Research proposal and supervisor acceptance required'
FROM PROGRAM WHERE program_name = 'Doctor of Philosophy (PhD) in Computer Science' AND level = 'PhD';

-- Doctor of Philosophy (PhD) in Information Technology
INSERT INTO ADMISSION_REQUIREMENT (program_id, qualification_type, minimum_grade, additional_requirements, entrance_exam_info)
SELECT program_id, 'Master', 'Minimum CGPA 3.00', 'Master degree in IT, Computer Science, or related field', 'Research proposal and supervisor acceptance required'
FROM PROGRAM WHERE program_name = 'Doctor of Philosophy (PhD) in Information Technology' AND level = 'PhD';

-- Doctor of Philosophy (PhD) in Actuarial Science
INSERT INTO ADMISSION_REQUIREMENT (program_id, qualification_type, minimum_grade, additional_requirements, entrance_exam_info)
SELECT program_id, 'Master', 'Minimum CGPA 3.00', 'Master degree in Actuarial Science, Mathematics, or Statistics', 'Research proposal and supervisor acceptance required'
FROM PROGRAM WHERE program_name = 'Doctor of Philosophy (PhD) in Actuarial Science' AND level = 'PhD';

-- Doctor of Philosophy (PhD) in Biotechnology
INSERT INTO ADMISSION_REQUIREMENT (program_id, qualification_type, minimum_grade, additional_requirements, entrance_exam_info)
SELECT program_id, 'Master', 'Minimum CGPA 3.00', 'Master degree in Biotechnology, Biology, or related field', 'Research proposal and supervisor acceptance required'
FROM PROGRAM WHERE program_name = 'Doctor of Philosophy (PhD) in Biotechnology' AND level = 'PhD';

-- Doctor of Philosophy (PhD) in Civil Engineering
INSERT INTO ADMISSION_REQUIREMENT (program_id, qualification_type, minimum_grade, additional_requirements, entrance_exam_info)
SELECT program_id, 'Master', 'Minimum CGPA 3.00', 'Master degree in Civil Engineering or related field. BEM registration preferred.', 'Research proposal and supervisor acceptance required'
FROM PROGRAM WHERE program_name = 'Doctor of Philosophy (PhD) in Civil Engineering' AND level = 'PhD';

INSERT INTO ADMISSION_REQUIREMENT (program_id, qualification_type, minimum_grade, additional_requirements, entrance_exam_info)
SELECT program_id, 'Bachelor', 'Minimum CGPA 3.67', 'First Class Honours Bachelor degree in Civil Engineering', 'Research proposal and supervisor acceptance required'
FROM PROGRAM WHERE program_name = 'Doctor of Philosophy (PhD) in Civil Engineering' AND level = 'PhD';

-- Doctor of Philosophy (PhD) in Electrical Engineering
INSERT INTO ADMISSION_REQUIREMENT (program_id, qualification_type, minimum_grade, additional_requirements, entrance_exam_info)
SELECT program_id, 'Master', 'Minimum CGPA 3.00', 'Master degree in Electrical Engineering or related field. BEM registration preferred.', 'Research proposal and supervisor acceptance required'
FROM PROGRAM WHERE program_name = 'Doctor of Philosophy (PhD) in Electrical Engineering' AND level = 'PhD';

INSERT INTO ADMISSION_REQUIREMENT (program_id, qualification_type, minimum_grade, additional_requirements, entrance_exam_info)
SELECT program_id, 'Bachelor', 'Minimum CGPA 3.67', 'First Class Honours Bachelor degree in Electrical Engineering', 'Research proposal and supervisor acceptance required'
FROM PROGRAM WHERE program_name = 'Doctor of Philosophy (PhD) in Electrical Engineering' AND level = 'PhD';

-- Verify the insertions
SELECT 
    p.program_id,
    p.program_name,
    p.level,
    f.faculty_name,
    COUNT(ar.requirement_id) as requirement_count
FROM PROGRAM p
JOIN FACULTY f ON p.faculty_id = f.faculty_id
LEFT JOIN ADMISSION_REQUIREMENT ar ON p.program_id = ar.program_id
WHERE p.level IN ('Master', 'PhD')
GROUP BY p.program_id, p.program_name, p.level, f.faculty_name
ORDER BY p.level, f.faculty_name, p.program_name;
