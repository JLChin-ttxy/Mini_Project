"""
Python script to add Foundation programs to the database
Run this with: python Database/add_foundation_now.py
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.db_helper import get_db_connection

def main():
    print("=" * 60)
    print("Adding Foundation Programs to Database")
    print("=" * 60)
    
    conn = get_db_connection()
    if not conn:
        print("❌ ERROR: Could not connect to database")
        print("Please check your database configuration in utils/db_helper.py")
        return False
    
    try:
        cursor = conn.cursor(dictionary=True)
        
        # Step 1: Check and update ENUM
        print("\n[Step 1] Checking ENUM...")
        cursor.execute("""
            SELECT COLUMN_TYPE 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_SCHEMA = DATABASE()
              AND TABLE_NAME = 'PROGRAM' 
              AND COLUMN_NAME = 'level'
        """)
        enum_result = cursor.fetchone()
        
        if enum_result:
            enum_type = enum_result['COLUMN_TYPE']
            print(f"   Current ENUM: {enum_type}")
            
            if 'Foundation' not in enum_type:
                print("   ⚠️  'Foundation' not in ENUM. Updating...")
                cursor.execute("""
                    ALTER TABLE PROGRAM 
                    MODIFY COLUMN level ENUM('Foundation', 'Diploma', 'Bachelor', 'Master', 'PhD') NOT NULL
                """)
                conn.commit()
                print("   ✅ ENUM updated successfully!")
            else:
                print("   ✅ 'Foundation' already in ENUM")
        else:
            print("   ⚠️  Could not check ENUM, attempting to update anyway...")
            try:
                cursor.execute("""
                    ALTER TABLE PROGRAM 
                    MODIFY COLUMN level ENUM('Foundation', 'Diploma', 'Bachelor', 'Master', 'PhD') NOT NULL
                """)
                conn.commit()
                print("   ✅ ENUM updated successfully!")
            except Exception as e:
                print(f"   ⚠️  Could not update ENUM: {e}")
        
        # Step 2: Add Foundation in Arts
        print("\n[Step 2] Adding Foundation in Arts...")
        cursor.execute("SELECT program_id FROM PROGRAM WHERE program_name = 'Foundation in Arts' AND level = 'Foundation'")
        if cursor.fetchone():
            print("   ✅ Foundation in Arts already exists")
        else:
            try:
                cursor.execute("""
                    INSERT INTO PROGRAM (faculty_id, program_name, level, duration_years, career_prospects, description) 
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (
                    2,  # Faculty of Arts and Social Science
                    'Foundation in Arts',
                    'Foundation',
                    1,
                    'Pathway to Bachelor programs in Arts, Social Science, Business, and Management',
                    'A comprehensive foundation program designed to prepare students for undergraduate studies in arts, social sciences, business, and management fields. Covers essential subjects including English, Mathematics, Business Studies, and Social Sciences.'
                ))
                conn.commit()
                print("   ✅ Foundation in Arts added successfully!")
            except Exception as e:
                print(f"   ❌ Error adding Foundation in Arts: {e}")
                return False
        
        # Step 3: Add Foundation in Science
        print("\n[Step 3] Adding Foundation in Science...")
        cursor.execute("SELECT program_id FROM PROGRAM WHERE program_name = 'Foundation in Science' AND level = 'Foundation'")
        if cursor.fetchone():
            print("   ✅ Foundation in Science already exists")
        else:
            try:
                cursor.execute("""
                    INSERT INTO PROGRAM (faculty_id, program_name, level, duration_years, career_prospects, description) 
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (
                    5,  # Faculty of Science
                    'Foundation in Science',
                    'Foundation',
                    1,
                    'Pathway to Bachelor programs in Science, Engineering, and Technology',
                    'A comprehensive foundation program designed to prepare students for undergraduate studies in science, engineering, and technology fields. Covers essential subjects including Mathematics, Physics, Chemistry, and Biology.'
                ))
                conn.commit()
                print("   ✅ Foundation in Science added successfully!")
            except Exception as e:
                print(f"   ❌ Error adding Foundation in Science: {e}")
                return False
        
        # Step 4: Verify
        print("\n[Step 4] Verifying Foundation programs...")
        cursor.execute("""
            SELECT p.program_id, p.program_name, p.level, f.faculty_name
            FROM PROGRAM p
            JOIN FACULTY f ON p.faculty_id = f.faculty_id
            WHERE p.level = 'Foundation'
            ORDER BY p.program_name
        """)
        foundation_programs = cursor.fetchall()
        
        print(f"\n   Found {len(foundation_programs)} Foundation program(s):")
        for prog in foundation_programs:
            print(f"   ✅ {prog['program_name']} (ID: {prog['program_id']}, Faculty: {prog['faculty_name']})")
        
        cursor.close()
        conn.close()
        
        print("\n" + "=" * 60)
        print("✅ SUCCESS! Foundation programs have been added.")
        print("   Please refresh the admission page to see them.")
        print("=" * 60)
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        if conn:
            conn.rollback()
            conn.close()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
