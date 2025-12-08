"""
Test MySQL Database Connection
Run this script to diagnose database connection issues
"""
import mysql.connector
from mysql.connector import Error

# Database configuration (same as in app.py)
DB_CONFIG = {
    'host': 'localhost',
    'database': 'university_admission_db',
    'user': 'root',
    'password': '123456',  
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_unicode_ci'
}

def test_connection():
    """Test database connection step by step"""
    print("=" * 60)
    print("MySQL Database Connection Test")
    print("=" * 60)
    
    # Step 1: Test connection without database
    print("\n[Step 1] Testing MySQL server connection (without database)...")
    try:
        config_no_db = DB_CONFIG.copy()
        config_no_db.pop('database', None)
        conn = mysql.connector.connect(**config_no_db)
        print("✓ MySQL server is running!")
        conn.close()
    except Error as e:
        print(f"✗ ERROR: Cannot connect to MySQL server")
        print(f"  Details: {e}")
        print("\n  Possible solutions:")
        print("  1. Make sure MySQL/MariaDB is installed")
        print("  2. Start MySQL service:")
        print("     - Windows: Open Services, find 'MySQL' and start it")
        print("     - Or run: net start MySQL (in Command Prompt as Administrator)")
        print("  3. Check if MySQL is running on port 3306")
        return False
    
    # Step 2: Check if database exists
    print("\n[Step 2] Checking if database 'university_admission_db' exists...")
    try:
        config_no_db = DB_CONFIG.copy()
        config_no_db.pop('database', None)
        conn = mysql.connector.connect(**config_no_db)
        cursor = conn.cursor()
        
        cursor.execute("SHOW DATABASES LIKE 'university_admission_db'")
        result = cursor.fetchone()
        
        if result:
            print("✓ Database 'university_admission_db' exists!")
        else:
            print("✗ Database 'university_admission_db' does NOT exist")
            print("\n  Creating database...")
            cursor.execute("CREATE DATABASE IF NOT EXISTS university_admission_db")
            conn.commit()
            print("✓ Database created successfully!")
            print("\n  Next steps:")
            print("  1. Run schema.sql to create tables:")
            print("     mysql -u root university_admission_db < Database/schema.sql")
            print("  2. Run data.sql to insert sample data:")
            print("     mysql -u root university_admission_db < Database/data.sql")
        
        cursor.close()
        conn.close()
    except Error as e:
        print(f"✗ ERROR: {e}")
        return False
    
    # Step 3: Test connection with database
    print("\n[Step 3] Testing connection to 'university_admission_db' database...")
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        print("✓ Successfully connected to database!")
        
        # Check if tables exist
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        
        if tables:
            print(f"✓ Found {len(tables)} table(s) in database")
            print("  Tables:", ", ".join([t[0] for t in tables]))
        else:
            print("⚠ Warning: Database exists but has no tables")
            print("  Run schema.sql to create tables")
        
        cursor.close()
        conn.close()
        print("\n" + "=" * 60)
        print("✓ All connection tests passed!")
        print("=" * 60)
        return True
        
    except Error as e:
        print(f"✗ ERROR: Cannot connect to database")
        print(f"  Details: {e}")
        print("\n  Possible solutions:")
        if "Access denied" in str(e):
            print("  1. Check your MySQL password in app.py and db_helper.py")
            print("  2. Default password is empty ('') - update if you set a password")
        elif "Unknown database" in str(e):
            print("  1. Database doesn't exist - it should have been created in Step 2")
        return False

if __name__ == '__main__':
    test_connection()

