-- Email Notification Subscriptions Table
-- Run this to add email notification functionality

USE university_admission_db;

CREATE TABLE IF NOT EXISTS EMAIL_NOTIFICATION (
    notification_id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(100) NOT NULL,
    program_id INT NOT NULL,
    notification_type ENUM('Deadline Reminder', 'Application Status', 'General') DEFAULT 'Deadline Reminder',
    days_before INT DEFAULT 14 COMMENT 'Number of days before deadline to send reminder',
    is_active BOOLEAN DEFAULT TRUE,
    subscribed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_sent TIMESTAMP NULL,
    FOREIGN KEY (program_id) REFERENCES PROGRAM(program_id) ON DELETE CASCADE,
    INDEX idx_email (email),
    INDEX idx_program (program_id),
    INDEX idx_active (is_active),
    UNIQUE KEY unique_subscription (email, program_id, notification_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Update existing records to use 14 days instead of 7
UPDATE EMAIL_NOTIFICATION SET days_before = 14 WHERE days_before = 7;

-- Update the default value for the column (if table already exists)
ALTER TABLE EMAIL_NOTIFICATION MODIFY COLUMN days_before INT DEFAULT 14 COMMENT 'Number of days before deadline to send reminder';
