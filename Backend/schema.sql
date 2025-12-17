-- ============================================================================
-- AI Chatbot for University Admission Inquiry System
-- Database Schema - MySQL/MariaDB (5 Modules Configuration)
-- Created: November 2025
-- Module 5 (Admission Status Tracking & Contact Support) has been removed
-- Contact information integrated into FACULTY table
-- ============================================================================

-- Create Database
CREATE DATABASE IF NOT EXISTS university_admission_db;
USE university_admission_db;

-- ============================================================================
-- CORE ACADEMIC TABLES (Module 1)
-- ============================================================================

-- Faculty/Department Table (Enhanced with contact information)
CREATE TABLE FACULTY (
    faculty_id INT AUTO_INCREMENT PRIMARY KEY,
    faculty_name VARCHAR(200) NOT NULL,
    description TEXT,
    contact_email VARCHAR(100),
    contact_phone VARCHAR(20),
    office_location VARCHAR(200),
    office_hours VARCHAR(100),
    location VARCHAR(200),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_faculty_name (faculty_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Academic Programs Table
CREATE TABLE PROGRAM (
    program_id INT AUTO_INCREMENT PRIMARY KEY,
    faculty_id INT NOT NULL,
    program_name VARCHAR(300) NOT NULL,
    level ENUM('Diploma', 'Bachelor', 'Master', 'PhD') NOT NULL,
    duration_years INT NOT NULL,
    career_prospects TEXT,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (faculty_id) REFERENCES FACULTY(faculty_id) ON DELETE CASCADE,
    INDEX idx_program_name (program_name),
    INDEX idx_level (level)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Faculty Members Table
CREATE TABLE FACULTY_MEMBER (
    member_id INT AUTO_INCREMENT PRIMARY KEY,
    faculty_id INT NOT NULL,
    name VARCHAR(200) NOT NULL,
    designation VARCHAR(100),
    specialization VARCHAR(300),
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(20),
    office_location VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (faculty_id) REFERENCES FACULTY(faculty_id) ON DELETE CASCADE,
    INDEX idx_member_name (name),
    INDEX idx_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Subjects/Courses Table
CREATE TABLE SUBJECT (
    subject_id INT AUTO_INCREMENT PRIMARY KEY,
    subject_code VARCHAR(20) UNIQUE NOT NULL,
    subject_name VARCHAR(300) NOT NULL,
    credit_hours INT NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_subject_code (subject_code)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Program-Subject Junction Table
CREATE TABLE PROGRAM_SUBJECT (
    program_id INT NOT NULL,
    subject_id INT NOT NULL,
    semester INT NOT NULL,
    is_mandatory BOOLEAN DEFAULT TRUE,
    PRIMARY KEY (program_id, subject_id),
    FOREIGN KEY (program_id) REFERENCES PROGRAM(program_id) ON DELETE CASCADE,
    FOREIGN KEY (subject_id) REFERENCES SUBJECT(subject_id) ON DELETE CASCADE,
    INDEX idx_semester (semester)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- ADMISSION RELATED TABLES (Module 2)
-- ============================================================================

-- Admission Requirements Table
CREATE TABLE ADMISSION_REQUIREMENT (
    requirement_id INT AUTO_INCREMENT PRIMARY KEY,
    program_id INT NOT NULL,
    qualification_type VARCHAR(100) NOT NULL,
    minimum_grade VARCHAR(100),
    additional_requirements TEXT,
    entrance_exam_info TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (program_id) REFERENCES PROGRAM(program_id) ON DELETE CASCADE,
    INDEX idx_qualification (qualification_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Applicants Table
CREATE TABLE APPLICANT (
    applicant_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(200) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20) NOT NULL,
    nationality VARCHAR(100),
    date_of_birth DATE,
    address TEXT,
    registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_name (full_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Applications Table
CREATE TABLE APPLICATION (
    application_id INT AUTO_INCREMENT PRIMARY KEY,
    applicant_id INT NOT NULL,
    program_id INT NOT NULL,
    reference_number VARCHAR(50) UNIQUE NOT NULL,
    status ENUM('Submitted', 'Under Review', 'Interview Scheduled', 'Accepted', 'Rejected', 'Withdrawn') DEFAULT 'Submitted',
    submission_date DATE NOT NULL,
    interview_date DATE,
    remarks TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (applicant_id) REFERENCES APPLICANT(applicant_id) ON DELETE CASCADE,
    FOREIGN KEY (program_id) REFERENCES PROGRAM(program_id) ON DELETE CASCADE,
    INDEX idx_reference (reference_number),
    INDEX idx_status (status),
    INDEX idx_submission_date (submission_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Application Status History Table (Moved from Module 5)
CREATE TABLE APPLICATION_STATUS (
    status_id INT AUTO_INCREMENT PRIMARY KEY,
    application_id INT NOT NULL,
    status VARCHAR(50) NOT NULL,
    remarks TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by INT,
    FOREIGN KEY (application_id) REFERENCES APPLICATION(application_id) ON DELETE CASCADE,
    INDEX idx_application (application_id),
    INDEX idx_updated_at (updated_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Document Checklist Table
CREATE TABLE DOCUMENT_CHECKLIST (
    checklist_id INT AUTO_INCREMENT PRIMARY KEY,
    program_id INT NOT NULL,
    document_name VARCHAR(200) NOT NULL,
    is_mandatory BOOLEAN DEFAULT TRUE,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (program_id) REFERENCES PROGRAM(program_id) ON DELETE CASCADE,
    INDEX idx_program (program_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Application Documents Table
CREATE TABLE APPLICATION_DOCUMENT (
    doc_id INT AUTO_INCREMENT PRIMARY KEY,
    application_id INT NOT NULL,
    checklist_id INT NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    verification_status ENUM('Pending', 'Verified', 'Rejected') DEFAULT 'Pending',
    FOREIGN KEY (application_id) REFERENCES APPLICATION(application_id) ON DELETE CASCADE,
    FOREIGN KEY (checklist_id) REFERENCES DOCUMENT_CHECKLIST(checklist_id) ON DELETE CASCADE,
    INDEX idx_application (application_id),
    INDEX idx_status (verification_status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Important Dates Table
CREATE TABLE IMPORTANT_DATE (
    date_id INT AUTO_INCREMENT PRIMARY KEY,
    program_id INT NOT NULL,
    event_type VARCHAR(100) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (program_id) REFERENCES PROGRAM(program_id) ON DELETE CASCADE,
    INDEX idx_program (program_id),
    INDEX idx_start_date (start_date),
    INDEX idx_event_type (event_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- FINANCIAL TABLES (Module 3)
-- ============================================================================

-- Tuition Fees Table
CREATE TABLE TUITION_FEE (
    fee_id INT AUTO_INCREMENT PRIMARY KEY,
    program_id INT NOT NULL,
    semester INT NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    currency VARCHAR(10) DEFAULT 'MYR',
    academic_year VARCHAR(10) NOT NULL,
    payment_deadline DATE,
    late_fee DECIMAL(10,2) DEFAULT 0.00,
    remarks TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (program_id) REFERENCES PROGRAM(program_id) ON DELETE CASCADE,
    INDEX idx_program (program_id),
    INDEX idx_semester (semester),
    INDEX idx_year (academic_year),
    INDEX idx_deadline (payment_deadline),
    CHECK (amount > 0),
    CHECK (late_fee >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Scholarships Table
CREATE TABLE SCHOLARSHIP (
    scholarship_id INT AUTO_INCREMENT PRIMARY KEY,
    scholarship_name VARCHAR(300) NOT NULL,
    eligibility_criteria TEXT NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    type VARCHAR(50),
    application_deadline DATE NOT NULL,
    available_slots INT,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_name (scholarship_name),
    INDEX idx_deadline (application_deadline),
    CHECK (amount > 0),
    CHECK (available_slots >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Scholarship Applications Table
CREATE TABLE SCHOLARSHIP_APPLICATION (
    scholarship_app_id INT AUTO_INCREMENT PRIMARY KEY,
    applicant_id INT NOT NULL,
    scholarship_id INT NOT NULL,
    application_date DATE NOT NULL,
    status ENUM('Submitted', 'Under Review', 'Approved', 'Rejected') DEFAULT 'Submitted',
    remarks TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (applicant_id) REFERENCES APPLICANT(applicant_id) ON DELETE CASCADE,
    FOREIGN KEY (scholarship_id) REFERENCES SCHOLARSHIP(scholarship_id) ON DELETE CASCADE,
    INDEX idx_applicant (applicant_id),
    INDEX idx_scholarship (scholarship_id),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Financial Aid Table
CREATE TABLE FINANCIAL_AID (
    aid_id INT AUTO_INCREMENT PRIMARY KEY,
    aid_name VARCHAR(200) NOT NULL,
    aid_type VARCHAR(100),
    eligibility_criteria TEXT,
    application_process TEXT,
    deadline DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_type (aid_type),
    INDEX idx_deadline (deadline)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- CAMPUS & FACILITIES TABLES (Module 4)
-- ============================================================================

-- Campus Facilities Table
CREATE TABLE CAMPUS_FACILITY (
    facility_id INT AUTO_INCREMENT PRIMARY KEY,
    facility_name VARCHAR(200) NOT NULL,
    facility_type VARCHAR(100),
    description TEXT,
    location VARCHAR(200),
    operating_hours VARCHAR(100),
    image_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_type (facility_type),
    INDEX idx_name (facility_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Accommodation/Hostel Table
CREATE TABLE ACCOMMODATION (
    accommodation_id INT AUTO_INCREMENT PRIMARY KEY,
    hostel_name VARCHAR(200) NOT NULL,
    room_type VARCHAR(50),
    monthly_fee DECIMAL(10,2) NOT NULL,
    capacity INT,
    available_slots INT,
    facilities TEXT,
    contact_info VARCHAR(200),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_hostel_name (hostel_name),
    INDEX idx_room_type (room_type),
    CHECK (monthly_fee > 0),
    CHECK (capacity >= 0),
    CHECK (available_slots >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Student Clubs Table
CREATE TABLE STUDENT_CLUB (
    club_id INT AUTO_INCREMENT PRIMARY KEY,
    club_name VARCHAR(200) NOT NULL,
    category VARCHAR(100),
    description TEXT,
    contact_person VARCHAR(200),
    contact_email VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_club_name (club_name),
    INDEX idx_category (category)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Campus Events Table
CREATE TABLE EVENT (
    event_id INT AUTO_INCREMENT PRIMARY KEY,
    event_name VARCHAR(300) NOT NULL,
    event_type VARCHAR(100),
    event_date DATE NOT NULL,
    location VARCHAR(200),
    description TEXT,
    organizer VARCHAR(200),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_event_date (event_date),
    INDEX idx_event_type (event_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- CHATBOT & USER INTERACTION TABLES (Module 6)
-- ============================================================================

-- Users Table
CREATE TABLE USER (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) UNIQUE,
    email VARCHAR(100) UNIQUE,
    user_type ENUM('Guest', 'Prospective Student', 'Applicant', 'Admin') DEFAULT 'Guest',
    registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_user_type (user_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Chat Sessions Table
CREATE TABLE CHAT_SESSION (
    session_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    end_time TIMESTAMP NULL,
    session_status ENUM('Active', 'Closed', 'Escalated') DEFAULT 'Active',
    ip_address VARCHAR(50),
    FOREIGN KEY (user_id) REFERENCES USER(user_id) ON DELETE SET NULL,
    INDEX idx_user (user_id),
    INDEX idx_status (session_status),
    INDEX idx_start_time (start_time)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Chat Messages Table
CREATE TABLE CHAT_MESSAGE (
    message_id INT AUTO_INCREMENT PRIMARY KEY,
    session_id INT NOT NULL,
    sender_type ENUM('User', 'Bot', 'Human Agent') NOT NULL,
    message_text TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    intent_detected VARCHAR(100),
    confidence_score DECIMAL(3,2),
    FOREIGN KEY (session_id) REFERENCES CHAT_SESSION(session_id) ON DELETE CASCADE,
    INDEX idx_session (session_id),
    INDEX idx_timestamp (timestamp),
    INDEX idx_intent (intent_detected),
    CHECK (confidence_score >= 0 AND confidence_score <= 1)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Feedback Table
CREATE TABLE FEEDBACK (
    feedback_id INT AUTO_INCREMENT PRIMARY KEY,
    session_id INT NOT NULL,
    rating INT NOT NULL,
    comment TEXT,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES CHAT_SESSION(session_id) ON DELETE CASCADE,
    INDEX idx_session (session_id),
    INDEX idx_rating (rating),
    CHECK (rating >= 1 AND rating <= 5)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- FAQ Table
CREATE TABLE FAQ (
    faq_id INT AUTO_INCREMENT PRIMARY KEY,
    category VARCHAR(100) NOT NULL,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    view_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_category (category),
    FULLTEXT idx_question (question)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- SAMPLE DATA INSERTION (Optional - for testing)
-- ============================================================================

-- Insert Sample Faculty
INSERT INTO FACULTY (faculty_name, description, contact_email, contact_phone, office_location, office_hours, location) VALUES
('Faculty of Computer Science and Information Technology', 'Leading faculty in computing education and research', 'fcsit@university.edu.my', '+60-3-1234-5678', 'A301, Block A', 'Mon-Fri: 9AM-5PM', 'Block A, Main Campus'),
('Faculty of Engineering', 'Excellence in engineering education', 'engineering@university.edu.my', '+60-3-1234-5679', 'B201, Block B', 'Mon-Fri: 9AM-5PM', 'Block B, Main Campus'),
('Faculty of Business and Economics', 'Developing future business leaders', 'fbe@university.edu.my', '+60-3-1234-5680', 'C101, Block C', 'Mon-Fri: 9AM-5PM', 'Block C, Main Campus');

-- Insert Sample Programs
INSERT INTO PROGRAM (faculty_id, program_name, level, duration_years, career_prospects, description) VALUES
(1, 'Bachelor of Computer Science (Artificial Intelligence)', 'Bachelor', 4, 'AI Engineer, Data Scientist, ML Researcher, Software Developer', 'Comprehensive program covering AI, machine learning, and data science'),
(1, 'Bachelor of Information Technology', 'Bachelor', 4, 'System Analyst, IT Consultant, Network Administrator', 'Focus on IT infrastructure and systems'),
(2, 'Bachelor of Engineering (Electrical)', 'Bachelor', 4, 'Electrical Engineer, Power Systems Engineer', 'Specialization in electrical systems'),
(3, 'Bachelor of Business Administration', 'Bachelor', 3, 'Business Analyst, Manager, Entrepreneur', 'Comprehensive business education');

-- Insert Sample FAQ
INSERT INTO FAQ (category, question, answer) VALUES
('General', 'What programs does the university offer?', 'The university offers programs at Diploma, Bachelor, Master, and PhD levels across various faculties including Computer Science, Engineering, Business, and more.'),
('Admission', 'How do I apply for admission?', 'You can apply online through our admission portal. Visit the Admissions page and click on Apply Now. You will need to prepare required documents and pay the application fee.'),
('Fees', 'What are the tuition fees?', 'Tuition fees vary by program and level. Bachelor programs typically range from RM 15,000 to RM 25,000 per year. Check specific program pages for detailed fee structures.'),
('Scholarship', 'Are scholarships available?', 'Yes, we offer merit-based and need-based scholarships. Eligibility criteria and deadlines vary. Visit the Scholarships page for detailed information.');

-- ============================================================================
-- END OF SCHEMA
-- ============================================================================

-- Verify table creation
SELECT 
    TABLE_NAME, 
    TABLE_ROWS, 
    CREATE_TIME 
FROM 
    information_schema.TABLES 
WHERE 
    TABLE_SCHEMA = 'university_admission_db'
ORDER BY 
    TABLE_NAME;
