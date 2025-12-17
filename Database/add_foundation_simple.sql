-- Simple SQL script to add Foundation programs
-- Run this in your MySQL client

USE university_admission_db;

-- Step 1: Update ENUM to include Foundation
ALTER TABLE PROGRAM MODIFY COLUMN level ENUM('Foundation', 'Diploma', 'Bachelor', 'Master', 'PhD') NOT NULL;

-- Step 2: Add Foundation in Arts (Faculty of Arts and Social Science - ID: 2)
INSERT INTO PROGRAM (faculty_id, program_name, level, duration_years, career_prospects, description) 
VALUES (2, 'Foundation in Arts', 'Foundation', 1, 
        'Pathway to Bachelor programs in Arts, Social Science, Business, and Management', 
        'A comprehensive foundation program designed to prepare students for undergraduate studies in arts, social sciences, business, and management fields. Covers essential subjects including English, Mathematics, Business Studies, and Social Sciences.')
ON DUPLICATE KEY UPDATE program_name = program_name;

-- Step 3: Add Foundation in Science (Faculty of Science - ID: 5)
INSERT INTO PROGRAM (faculty_id, program_name, level, duration_years, career_prospects, description) 
VALUES (5, 'Foundation in Science', 'Foundation', 1, 
        'Pathway to Bachelor programs in Science, Engineering, and Technology', 
        'A comprehensive foundation program designed to prepare students for undergraduate studies in science, engineering, and technology fields. Covers essential subjects including Mathematics, Physics, Chemistry, and Biology.')
ON DUPLICATE KEY UPDATE program_name = program_name;

-- Step 4: Verify
SELECT program_id, program_name, level, 
       (SELECT faculty_name FROM FACULTY WHERE FACULTY.faculty_id = PROGRAM.faculty_id) as faculty_name
FROM PROGRAM 
WHERE level = 'Foundation'
ORDER BY program_name;
