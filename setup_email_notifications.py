"""
Quick script to set up email notifications table
Run this: python setup_email_notifications.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from utils.db_helper import get_db_connection

def setup_email_table():
    """Create the EMAIL_NOTIFICATION table"""
    print("Setting up EMAIL_NOTIFICATION table...")
    
    conn = get_db_connection()
    if not conn:
        print("ERROR: Could not connect to database!")
        print("Please check your database connection settings in utils/db_helper.py")
        return False
    
    try:
        cursor = conn.cursor()
        
        # Create the table
        create_table_sql = """
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
        """
        
        print("Creating EMAIL_NOTIFICATION table...")
        cursor.execute(create_table_sql)
        conn.commit()
        print("✓ Table created successfully!")
        
        # Verify
        cursor.execute("SHOW TABLES LIKE 'EMAIL_NOTIFICATION'")
        if cursor.fetchone():
            print("✓ Table verified!")
            cursor.close()
            conn.close()
            print("\n✅ Email notifications are now set up!")
            print("You can now subscribe to email reminders on the deadlines page.")
            return True
        else:
            print("✗ Table was not created!")
            return False
            
    except Exception as e:
        print(f"✗ ERROR: {e}")
        if "already exists" in str(e).lower():
            print("(Table might already exist - this is okay)")
            return True
        return False
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    success = setup_email_table()
    sys.exit(0 if success else 1)
