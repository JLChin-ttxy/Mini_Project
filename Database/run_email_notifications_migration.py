"""
Run Email Notifications Migration
This script creates the EMAIL_NOTIFICATION table in the database
"""
import mysql.connector
from mysql.connector import Error
import os

# Database configuration (same as in utils/db_helper.py)
DB_CONFIG = {
    'host': 'localhost',
    'database': 'university_admission_db',
    'user': 'root',
    'password': '123456',  # Update this if your MySQL password is different
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_unicode_ci'
}

def run_migration():
    """Run the email notifications migration SQL file"""
    print("=" * 60)
    print("Email Notifications Migration")
    print("=" * 60)
    
    # Read the SQL file
    sql_file_path = os.path.join(os.path.dirname(__file__), 'email_notifications_migration.sql')
    
    if not os.path.exists(sql_file_path):
        print(f"✗ ERROR: SQL file not found at: {sql_file_path}")
        return False
    
    try:
        # Connect to database
        print("\n[Step 1] Connecting to MySQL database...")
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        print("✓ Connected successfully!")
        
        # Read and execute SQL file
        print("\n[Step 2] Reading SQL migration file...")
        with open(sql_file_path, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        print("✓ SQL file read successfully!")
        
        # Split SQL into individual statements
        print("\n[Step 3] Executing SQL statements...")
        statements = [s.strip() for s in sql_content.split(';') if s.strip() and not s.strip().startswith('--')]
        
        for i, statement in enumerate(statements, 1):
            if statement:
                try:
                    cursor.execute(statement)
                    print(f"  ✓ Statement {i} executed successfully")
                except Error as e:
                    # Some statements might fail if table already exists, which is okay
                    if "already exists" in str(e).lower() or "duplicate" in str(e).lower():
                        print(f"  ⚠ Statement {i} skipped (already exists): {str(e)[:50]}")
                    else:
                        print(f"  ✗ Statement {i} failed: {e}")
                        raise
        
        # Commit changes
        conn.commit()
        print("\n✓ All statements executed successfully!")
        
        # Verify table was created
        print("\n[Step 4] Verifying EMAIL_NOTIFICATION table...")
        cursor.execute("SHOW TABLES LIKE 'EMAIL_NOTIFICATION'")
        result = cursor.fetchone()
        
        if result:
            print("✓ EMAIL_NOTIFICATION table exists!")
            
            # Show table structure
            cursor.execute("DESCRIBE EMAIL_NOTIFICATION")
            columns = cursor.fetchall()
            print("\nTable structure:")
            for col in columns:
                print(f"  - {col[0]}: {col[1]}")
        else:
            print("✗ WARNING: EMAIL_NOTIFICATION table not found after migration!")
            return False
        
        cursor.close()
        conn.close()
        
        print("\n" + "=" * 60)
        print("Migration completed successfully!")
        print("=" * 60)
        print("\nYou can now use the email subscription feature.")
        return True
        
    except Error as e:
        print(f"\n✗ ERROR: {e}")
        print("\nPossible solutions:")
        print("1. Make sure MySQL is running")
        print("2. Check your database password in the script (line 13)")
        print("3. Make sure the database 'university_admission_db' exists")
        return False

if __name__ == '__main__':
    success = run_migration()
    if not success:
        print("\nMigration failed. Please check the errors above.")
        exit(1)
