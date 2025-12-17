# Setup Email Notifications Table

## Quick Setup (Choose One Method)

### Method 1: Run Python Script (Easiest)
```bash
python setup_email_notifications.py
```

### Method 2: Using MySQL Command Line
```bash
mysql -u root -p university_admission_db < Database/email_notifications_migration.sql
```

### Method 3: Using MySQL Workbench
1. Open MySQL Workbench
2. Connect to your MySQL server
3. Open `Database/email_notifications_migration.sql`
4. Click Execute (⚡ button)

### Method 4: Manual SQL Execution
Connect to MySQL and run:

```sql
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
```

## Verify Setup

After running the migration, verify the table exists:

```sql
SHOW TABLES LIKE 'EMAIL_NOTIFICATION';
DESCRIBE EMAIL_NOTIFICATION;
```

## Troubleshooting

**If you get "Table already exists" error:**
- This is okay! The table is already set up.
- You can proceed to use the email subscription feature.

**If you get "Database connection failed":**
- Check that MySQL is running
- Verify your database password in `utils/db_helper.py`
- Make sure the database `university_admission_db` exists
