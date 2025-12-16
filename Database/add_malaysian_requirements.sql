-- Add more Malaysian qualification requirements (UEC, Matriculation, Foundation) to programs
-- This ensures all programs have comprehensive Malaysian student requirements

USE university_admission_db;

-- Add UEC requirements to programs that don't have them
INSERT INTO ADMISSION_REQUIREMENT (program_id, qualification_type, minimum_grade, additional_requirements, entrance_exam_info)
SELECT p.program_id, 'UEC', 
       CASE 
           WHEN p.level = 'Bachelor' THEN 'Minimum 5Bs including relevant subjects'
           WHEN p.level = 'Diploma' THEN 'Minimum 5Cs including relevant subjects'
           WHEN p.level = 'Master' THEN 'Bachelor degree required (UEC not applicable)'
           WHEN p.level = 'PhD' THEN 'Master degree required (UEC not applicable)'
           ELSE 'Minimum 5Bs'
       END,
       CASE 
           WHEN f.faculty_name LIKE '%Engineering%' THEN 'Must include Mathematics and Physics'
           WHEN f.faculty_name LIKE '%Computer%' OR f.faculty_name LIKE '%IT%' THEN 'Must include Mathematics'
           WHEN f.faculty_name LIKE '%Science%' THEN 'Must include Mathematics and Science subjects'
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

-- Add Matriculation requirements to Science/Engineering programs
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
           ELSE NULL
       END,
       NULL
FROM PROGRAM p
JOIN FACULTY f ON p.faculty_id = f.faculty_id
WHERE (f.faculty_name LIKE '%Engineering%' OR f.faculty_name LIKE '%Science%')
  AND p.level IN ('Bachelor', 'Diploma')
  AND NOT EXISTS (
      SELECT 1 FROM ADMISSION_REQUIREMENT ar 
      WHERE ar.program_id = p.program_id 
      AND ar.qualification_type = 'Matriculation'
  );

-- Add Foundation requirements to programs that don't have them
INSERT INTO ADMISSION_REQUIREMENT (program_id, qualification_type, minimum_grade, additional_requirements, entrance_exam_info)
SELECT p.program_id, 'Foundation',
       CASE 
           WHEN p.level = 'Bachelor' THEN 'Minimum CGPA 2.00 in relevant field'
           WHEN p.level = 'Diploma' THEN 'Minimum CGPA 2.00'
           ELSE 'Minimum CGPA 2.00'
       END,
       'Foundation studies in relevant field',
       NULL
FROM PROGRAM p
WHERE p.level IN ('Bachelor', 'Diploma')
  AND NOT EXISTS (
      SELECT 1 FROM ADMISSION_REQUIREMENT ar 
      WHERE ar.program_id = p.program_id 
      AND ar.qualification_type = 'Foundation'
  )
LIMIT 20; -- Limit to avoid duplicates if some already exist

