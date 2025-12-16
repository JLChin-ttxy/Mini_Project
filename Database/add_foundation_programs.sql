-- ============================================================================
-- Add Foundation Programs: Foundation in Art and Foundation in Science
-- ============================================================================

USE university_admission_db;

-- First, update the ENUM to include 'Foundation' as a valid level
-- Note: MySQL/MariaDB requires modifying the ENUM to add new values
ALTER TABLE PROGRAM MODIFY COLUMN level ENUM('Foundation', 'Diploma', 'Bachelor', 'Master', 'PhD') NOT NULL;

-- Add Foundation in Arts program
-- We'll assign it to Faculty of Arts and Social Science (faculty_id = 2)
-- Check if it already exists first
INSERT INTO PROGRAM (faculty_id, program_name, level, duration_years, career_prospects, description) 
SELECT 2, 'Foundation in Arts', 'Foundation', 1, 
       'Pathway to Bachelor programs in Arts, Social Science, Business, and Management', 
       'A comprehensive foundation program designed to prepare students for undergraduate studies in arts, social sciences, business, and management fields. Covers essential subjects including English, Mathematics, Business Studies, and Social Sciences.'
WHERE NOT EXISTS (
    SELECT 1 FROM PROGRAM 
    WHERE program_name = 'Foundation in Arts' AND level = 'Foundation'
);

-- Add Foundation in Science program  
-- We'll assign it to Faculty of Science (faculty_id = 5)
-- Check if it already exists first
INSERT INTO PROGRAM (faculty_id, program_name, level, duration_years, career_prospects, description) 
SELECT 5, 'Foundation in Science', 'Foundation', 1, 
       'Pathway to Bachelor programs in Science, Engineering, and Technology', 
       'A comprehensive foundation program designed to prepare students for undergraduate studies in science, engineering, and technology fields. Covers essential subjects including Mathematics, Physics, Chemistry, and Biology.'
WHERE NOT EXISTS (
    SELECT 1 FROM PROGRAM 
    WHERE program_name = 'Foundation in Science' AND level = 'Foundation'
);

-- Verify the programs were added
SELECT program_id, program_name, level, faculty_id, 
       (SELECT faculty_name FROM FACULTY WHERE FACULTY.faculty_id = PROGRAM.faculty_id) as faculty_name
FROM PROGRAM 
WHERE level = 'Foundation'
ORDER BY program_name;
