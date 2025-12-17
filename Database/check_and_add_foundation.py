"""
Quick script to check and add Foundation programs
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.db_helper import get_db_connection

conn = get_db_connection()
if not conn:
    print("ERROR: No database connection")
    sys.exit(1)

cursor = conn.cursor(dictionary=True)

# Check current ENUM
cursor.execute("""
    SELECT COLUMN_TYPE 
    FROM INFORMATION_SCHEMA.COLUMNS 
    WHERE TABLE_SCHEMA = DATABASE()
      AND TABLE_NAME = 'PROGRAM' 
      AND COLUMN_NAME = 'level'
""")
enum_result = cursor.fetchone()
print(f"Current ENUM: {enum_result['COLUMN_TYPE'] if enum_result else 'Not found'}")

# Check if Foundation programs exist
cursor.execute("SELECT program_id, program_name, level FROM PROGRAM WHERE program_name LIKE '%Foundation%'")
existing = cursor.fetchall()
print(f"\nExisting Foundation programs: {len(existing)}")
for prog in existing:
    print(f"  - {prog['program_name']} (ID: {prog['program_id']}, Level: {prog['level']})")

# Update ENUM if needed
if enum_result and 'Foundation' not in enum_result['COLUMN_TYPE']:
    print("\nUpdating ENUM to include Foundation...")
    cursor.execute("""
        ALTER TABLE PROGRAM 
        MODIFY COLUMN level ENUM('Foundation', 'Diploma', 'Bachelor', 'Master', 'PhD') NOT NULL
    """)
    conn.commit()
    print("✓ ENUM updated")

# Add Foundation in Arts if it doesn't exist
cursor.execute("SELECT program_id FROM PROGRAM WHERE program_name = 'Foundation in Arts'")
if not cursor.fetchone():
    print("\nAdding Foundation in Arts...")
    cursor.execute("""
        INSERT INTO PROGRAM (faculty_id, program_name, level, duration_years, career_prospects, description) 
        VALUES (2, 'Foundation in Arts', 'Foundation', 1, 
                'Pathway to Bachelor programs in Arts, Social Science, Business, and Management', 
                'A comprehensive foundation program designed to prepare students for undergraduate studies in arts, social sciences, business, and management fields. Covers essential subjects including English, Mathematics, Business Studies, and Social Sciences.')
    """)
    conn.commit()
    print("✓ Added Foundation in Arts")
else:
    print("\n✓ Foundation in Arts already exists")

# Add Foundation in Science if it doesn't exist
cursor.execute("SELECT program_id FROM PROGRAM WHERE program_name = 'Foundation in Science'")
if not cursor.fetchone():
    print("\nAdding Foundation in Science...")
    cursor.execute("""
        INSERT INTO PROGRAM (faculty_id, program_name, level, duration_years, career_prospects, description) 
        VALUES (5, 'Foundation in Science', 'Foundation', 1, 
                'Pathway to Bachelor programs in Science, Engineering, and Technology', 
                'A comprehensive foundation program designed to prepare students for undergraduate studies in science, engineering, and technology fields. Covers essential subjects including Mathematics, Physics, Chemistry, and Biology.')
    """)
    conn.commit()
    print("✓ Added Foundation in Science")
else:
    print("\n✓ Foundation in Science already exists")

# Final check
cursor.execute("""
    SELECT p.program_id, p.program_name, p.level, f.faculty_name
    FROM PROGRAM p
    JOIN FACULTY f ON p.faculty_id = f.faculty_id
    WHERE p.level = 'Foundation'
    ORDER BY p.program_name
""")
final = cursor.fetchall()
print(f"\n=== Final Foundation Programs ({len(final)}) ===")
for prog in final:
    print(f"  - {prog['program_name']} (Faculty: {prog['faculty_name']})")

cursor.close()
conn.close()
print("\n✓ Done!")
