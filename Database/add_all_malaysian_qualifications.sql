-- Add comprehensive Malaysian qualification requirements to all programs
-- Includes: UEC, STPM, SPM, Foundation, SAM, Matriculation, A-Level, Diploma

USE university_admission_db;

-- Function to add qualification if it doesn't exist
-- We'll add qualifications based on program level and faculty

-- Add SPM requirements (for Foundation/Diploma programs)
INSERT INTO ADMISSION_REQUIREMENT (program_id, qualification_type, minimum_grade, additional_requirements, entrance_exam_info)
SELECT p.program_id, 'SPM',
       CASE 
           WHEN p.level = 'Diploma' THEN 'Minimum 3 Credits including relevant subjects'
           WHEN p.level = 'Foundation' THEN 'Minimum 5 Credits including Mathematics and English'
           ELSE 'Minimum 5 Credits including relevant subjects'
       END,
       CASE 
           WHEN f.faculty_name LIKE '%Engineering%' THEN 'Credit in Mathematics and Science'
           WHEN f.faculty_name LIKE '%Computer%' OR f.faculty_name LIKE '%IT%' THEN 'Credit in Mathematics'
           WHEN f.faculty_name LIKE '%Business%' THEN 'Credit in Mathematics and English'
           ELSE 'Credit in relevant subjects'
       END,
       NULL
FROM PROGRAM p
JOIN FACULTY f ON p.faculty_id = f.faculty_id
WHERE p.level IN ('Diploma', 'Foundation')
  AND NOT EXISTS (
      SELECT 1 FROM ADMISSION_REQUIREMENT ar 
      WHERE ar.program_id = p.program_id 
      AND ar.qualification_type = 'SPM'
  );

-- Add SAM (South Australian Matriculation) requirements
INSERT INTO ADMISSION_REQUIREMENT (program_id, qualification_type, minimum_grade, additional_requirements, entrance_exam_info)
SELECT p.program_id, 'SAM',
       CASE 
           WHEN p.level = 'Bachelor' THEN 'ATAR 70 and Grade B in 2 relevant subjects'
           WHEN p.level = 'Diploma' THEN 'ATAR 60 and Grade C in 2 relevant subjects'
           ELSE 'ATAR 70 and Grade B in 2 relevant subjects'
       END,
       CASE 
           WHEN f.faculty_name LIKE '%Engineering%' THEN 'Must include Mathematics and Physics'
           WHEN f.faculty_name LIKE '%Computer%' OR f.faculty_name LIKE '%IT%' THEN 'Must include Mathematics'
           WHEN f.faculty_name LIKE '%Science%' THEN 'Must include Mathematics and Science'
           WHEN f.faculty_name LIKE '%Business%' THEN 'Must include Mathematics'
           ELSE NULL
       END,
       NULL
FROM PROGRAM p
JOIN FACULTY f ON p.faculty_id = f.faculty_id
WHERE p.level IN ('Bachelor', 'Diploma')
  AND NOT EXISTS (
      SELECT 1 FROM ADMISSION_REQUIREMENT ar 
      WHERE ar.program_id = p.program_id 
      AND ar.qualification_type = 'SAM'
  );

-- Add UEC to programs that don't have it
INSERT INTO ADMISSION_REQUIREMENT (program_id, qualification_type, minimum_grade, additional_requirements, entrance_exam_info)
SELECT p.program_id, 'UEC',
       CASE 
           WHEN p.level = 'Bachelor' THEN 'Minimum 5Bs including relevant subjects'
           WHEN p.level = 'Diploma' THEN 'Minimum 5Cs including relevant subjects'
           ELSE 'Minimum 5Bs'
       END,
       CASE 
           WHEN f.faculty_name LIKE '%Engineering%' THEN 'Must include Mathematics and Physics'
           WHEN f.faculty_name LIKE '%Computer%' OR f.faculty_name LIKE '%IT%' THEN 'Must include Mathematics'
           WHEN f.faculty_name LIKE '%Science%' THEN 'Must include Mathematics and Science'
           WHEN f.faculty_name LIKE '%Business%' THEN 'Must include Mathematics'
           ELSE NULL
       END,
       NULL
FROM PROGRAM p
JOIN FACULTY f ON p.faculty_id = f.faculty_id
WHERE p.level IN ('Bachelor', 'Diploma')
  AND NOT EXISTS (
      SELECT 1 FROM ADMISSION_REQUIREMENT ar 
      WHERE ar.program_id = p.program_id 
      AND ar.qualification_type = 'UEC'
  );

-- Add Foundation to programs that don't have it
INSERT INTO ADMISSION_REQUIREMENT (program_id, qualification_type, minimum_grade, additional_requirements, entrance_exam_info)
SELECT p.program_id, 'Foundation',
       CASE 
           WHEN p.level = 'Bachelor' THEN 'Minimum CGPA 2.00 in relevant field'
           WHEN p.level = 'Diploma' THEN 'Minimum CGPA 2.00'
           ELSE 'Minimum CGPA 2.00'
       END,
       'Foundation studies in relevant field from recognized institutions',
       NULL
FROM PROGRAM p
WHERE p.level IN ('Bachelor', 'Diploma')
  AND NOT EXISTS (
      SELECT 1 FROM ADMISSION_REQUIREMENT ar 
      WHERE ar.program_id = p.program_id 
      AND ar.qualification_type = 'Foundation'
  );

-- Add Matriculation to Science/Engineering programs that don't have it
INSERT INTO ADMISSION_REQUIREMENT (program_id, qualification_type, minimum_grade, additional_requirements, entrance_exam_info)
SELECT p.program_id, 'Matriculation',
       CASE 
           WHEN p.level = 'Bachelor' THEN 'Minimum CGPA 2.00 in Science/Engineering stream'
           WHEN p.level = 'Diploma' THEN 'Minimum CGPA 2.00'
           ELSE 'Minimum CGPA 2.00'
       END,
       CASE 
           WHEN f.faculty_name LIKE '%Engineering%' THEN 'Science stream with Mathematics and Physics'
           WHEN f.faculty_name LIKE '%Science%' THEN 'Science stream'
           WHEN f.faculty_name LIKE '%Computer%' OR f.faculty_name LIKE '%IT%' THEN 'Science stream with Mathematics'
           ELSE 'Science stream'
       END,
       NULL
FROM PROGRAM p
JOIN FACULTY f ON p.faculty_id = f.faculty_id
WHERE (f.faculty_name LIKE '%Engineering%' OR f.faculty_name LIKE '%Science%' OR f.faculty_name LIKE '%Computer%' OR f.faculty_name LIKE '%IT%')
  AND p.level IN ('Bachelor', 'Diploma')
  AND NOT EXISTS (
      SELECT 1 FROM ADMISSION_REQUIREMENT ar 
      WHERE ar.program_id = p.program_id 
      AND ar.qualification_type = 'Matriculation'
  );

-- Add A-Level to programs that don't have it
INSERT INTO ADMISSION_REQUIREMENT (program_id, qualification_type, minimum_grade, additional_requirements, entrance_exam_info)
SELECT p.program_id, 'A-Level',
       CASE 
           WHEN p.level = 'Bachelor' THEN 'Minimum Grade D in 2 subjects'
           WHEN p.level = 'Diploma' THEN 'Minimum Grade E in 2 subjects'
           ELSE 'Minimum Grade D in 2 subjects'
       END,
       CASE 
           WHEN f.faculty_name LIKE '%Engineering%' THEN 'Must include Mathematics and Physics'
           WHEN f.faculty_name LIKE '%Computer%' OR f.faculty_name LIKE '%IT%' THEN 'Must include Mathematics'
           WHEN f.faculty_name LIKE '%Science%' THEN 'Must include Mathematics and Science'
           WHEN f.faculty_name LIKE '%Business%' THEN 'Must include Mathematics'
           ELSE NULL
       END,
       NULL
FROM PROGRAM p
JOIN FACULTY f ON p.faculty_id = f.faculty_id
WHERE p.level IN ('Bachelor', 'Diploma')
  AND NOT EXISTS (
      SELECT 1 FROM ADMISSION_REQUIREMENT ar 
      WHERE ar.program_id = p.program_id 
      AND ar.qualification_type = 'A-Level'
  );

-- Add Diploma to programs that don't have it (for credit transfer)
INSERT INTO ADMISSION_REQUIREMENT (program_id, qualification_type, minimum_grade, additional_requirements, entrance_exam_info)
SELECT p.program_id, 'Diploma',
       CASE 
           WHEN p.level = 'Bachelor' THEN 'Minimum CGPA 2.50 in relevant field'
           ELSE 'Minimum CGPA 2.50'
       END,
       'Diploma (Level 4, MQF) in relevant field. Credit transfer may be available.',
       NULL
FROM PROGRAM p
WHERE p.level = 'Bachelor'
  AND NOT EXISTS (
      SELECT 1 FROM ADMISSION_REQUIREMENT ar 
      WHERE ar.program_id = p.program_id 
      AND ar.qualification_type = 'Diploma'
  );

-- Ensure STPM exists for all Bachelor programs
INSERT INTO ADMISSION_REQUIREMENT (program_id, qualification_type, minimum_grade, additional_requirements, entrance_exam_info)
SELECT p.program_id, 'STPM',
       CASE 
           WHEN p.level = 'Bachelor' THEN 'Minimum Grade C in 2 subjects (CGPA 2.00)'
           WHEN p.level = 'Diploma' THEN 'Minimum Grade C in 1 subject'
           ELSE 'Minimum Grade C in 2 subjects'
       END,
       CASE 
           WHEN f.faculty_name LIKE '%Engineering%' THEN 'Credit in Mathematics and Additional Mathematics at SPM level'
           WHEN f.faculty_name LIKE '%Computer%' OR f.faculty_name LIKE '%IT%' THEN 'Credit in Mathematics at SPM level'
           WHEN f.faculty_name LIKE '%Science%' THEN 'Credit in Mathematics and Science at SPM level'
           WHEN f.faculty_name LIKE '%Business%' THEN 'Credit in Mathematics at SPM level'
           ELSE 'Credit in relevant subjects at SPM level'
       END,
       'No entrance exam required'
FROM PROGRAM p
JOIN FACULTY f ON p.faculty_id = f.faculty_id
WHERE p.level IN ('Bachelor', 'Diploma')
  AND NOT EXISTS (
      SELECT 1 FROM ADMISSION_REQUIREMENT ar 
      WHERE ar.program_id = p.program_id 
      AND ar.qualification_type = 'STPM'
  );

