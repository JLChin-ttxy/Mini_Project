-- Run this SQL script to add Foundation programs
-- Copy and paste into your MySQL client

USE university_admission_db;

-- Step 1: Update ENUM
ALTER TABLE PROGRAM MODIFY COLUMN level ENUM('Foundation', 'Diploma', 'Bachelor', 'Master', 'PhD') NOT NULL;

-- Step 2: Add Foundation in Arts
INSERT IGNORE INTO PROGRAM (faculty_id, program_name, level, duration_years, career_prospects, description) 
VALUES (2, 'Foundation in Arts', 'Foundation', 1, 
        'Pathway to Bachelor programs in Arts, Social Science, Business, and Management', 
        'A comprehensive foundation program designed to prepare students for undergraduate studies in arts, social sciences, business, and management fields. Covers essential subjects including English, Mathematics, Business Studies, and Social Sciences.');

-- Step 3: Add Foundation in Science
INSERT IGNORE INTO PROGRAM (faculty_id, program_name, level, duration_years, career_prospects, description) 
VALUES (5, 'Foundation in Science', 'Foundation', 1, 
        'Pathway to Bachelor programs in Science, Engineering, and Technology', 
        'A comprehensive foundation program designed to prepare students for undergraduate studies in science, engineering, and technology fields. Covers essential subjects including Mathematics, Physics, Chemistry, and Biology.');

-- Step 4: Verify
SELECT program_id, program_name, level, 
       (SELECT faculty_name FROM FACULTY WHERE FACULTY.faculty_id = PROGRAM.faculty_id) as faculty_name
FROM PROGRAM 
WHERE level = 'Foundation'
ORDER BY program_name;
