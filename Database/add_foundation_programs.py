"""
Script to add Foundation in Arts and Foundation in Science programs
"""
import sys
import os

# Add parent directory to path to import utils
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.db_helper import get_db_connection

def add_foundation_programs():
    """Add Foundation in Arts and Foundation in Science programs"""
    conn = get_db_connection()
    if not conn:
        print("Error: Could not connect to database")
        return False
    
    try:
        cursor = conn.cursor()
        
        # First, check if Foundation is in the ENUM
        try:
            cursor.execute("""
                SELECT COLUMN_TYPE 
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_SCHEMA = DATABASE()
                  AND TABLE_NAME = 'PROGRAM' 
                  AND COLUMN_NAME = 'level'
            """)
            enum_result = cursor.fetchone()
            if enum_result:
                enum_type = enum_result[0]
                print(f"Current level ENUM: {enum_type}")
                
                # Check if Foundation is already in the ENUM
                if 'Foundation' not in enum_type:
                    print("Adding 'Foundation' to the level ENUM...")
                    cursor.execute("""
                        ALTER TABLE PROGRAM 
                        MODIFY COLUMN level ENUM('Foundation', 'Diploma', 'Bachelor', 'Master', 'PhD') NOT NULL
                    """)
                    conn.commit()
                    print("✓ Successfully added 'Foundation' to level ENUM")
                else:
                    print("✓ 'Foundation' already exists in level ENUM")
        except Exception as e:
            print(f"Note: Could not check ENUM (may need manual update): {e}")
        
        # Check if Foundation in Arts already exists
        cursor.execute("""
            SELECT program_id FROM PROGRAM 
            WHERE program_name = 'Foundation in Arts' AND level = 'Foundation'
        """)
        if cursor.fetchone():
            print("✓ Foundation in Arts already exists")
        else:
            # Add Foundation in Arts (assign to Faculty of Arts and Social Science - faculty_id = 2)
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
            print("✓ Successfully added Foundation in Arts")
        
        # Check if Foundation in Science already exists
        cursor.execute("""
            SELECT program_id FROM PROGRAM 
            WHERE program_name = 'Foundation in Science' AND level = 'Foundation'
        """)
        if cursor.fetchone():
            print("✓ Foundation in Science already exists")
        else:
            # Add Foundation in Science (assign to Faculty of Science - faculty_id = 5)
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
            print("✓ Successfully added Foundation in Science")
        
        # Verify the programs
        cursor.execute("""
            SELECT p.program_id, p.program_name, p.level, f.faculty_name
            FROM PROGRAM p
            JOIN FACULTY f ON p.faculty_id = f.faculty_id
            WHERE p.level = 'Foundation'
            ORDER BY p.program_name
        """)
        foundation_programs = cursor.fetchall()
        
        print("\n=== Foundation Programs ===")
        for program in foundation_programs:
            print(f"ID: {program[0]}, Name: {program[1]}, Level: {program[2]}, Faculty: {program[3]}")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        if conn:
            conn.rollback()
            conn.close()
        return False

if __name__ == "__main__":
    print("Adding Foundation programs...")
    success = add_foundation_programs()
    if success:
        print("\n✓ All foundation programs added successfully!")
    else:
        print("\n✗ Failed to add foundation programs")
        sys.exit(1)
