"""Verify and add Foundation programs"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.db_helper import get_db_connection

# Force unbuffered output
sys.stdout.reconfigure(line_buffering=True) if hasattr(sys.stdout, 'reconfigure') else None

conn = get_db_connection()
if not conn:
    print("ERROR: No database connection", flush=True)
    sys.exit(1)

cursor = conn.cursor(dictionary=True)

# Check ENUM
cursor.execute("""
    SELECT COLUMN_TYPE 
    FROM INFORMATION_SCHEMA.COLUMNS 
    WHERE TABLE_SCHEMA = DATABASE()
      AND TABLE_NAME = 'PROGRAM' 
      AND COLUMN_NAME = 'level'
""")
enum = cursor.fetchone()
print("ENUM:", enum['COLUMN_TYPE'] if enum else "Not found", flush=True)

# Check existing programs
cursor.execute("SELECT program_id, program_name, level FROM PROGRAM WHERE program_name LIKE '%Foundation%' OR level = 'Foundation'")
existing = cursor.fetchall()
print(f"\nExisting Foundation-related programs: {len(existing)}")
for p in existing:
    print(f"  ID: {p['program_id']}, Name: {p['program_name']}, Level: {p['level']}")

# Update ENUM if needed
if enum and 'Foundation' not in enum['COLUMN_TYPE']:
    print("\n⚠️  Foundation not in ENUM! Updating...")
    try:
        cursor.execute("ALTER TABLE PROGRAM MODIFY COLUMN level ENUM('Foundation', 'Diploma', 'Bachelor', 'Master', 'PhD') NOT NULL")
        conn.commit()
        print("✓ ENUM updated")
    except Exception as e:
        print(f"✗ Error updating ENUM: {e}")

# Add Foundation in Arts
cursor.execute("SELECT program_id FROM PROGRAM WHERE program_name = 'Foundation in Arts'")
if not cursor.fetchone():
    print("\n➕ Adding Foundation in Arts...")
    try:
        cursor.execute("""
            INSERT INTO PROGRAM (faculty_id, program_name, level, duration_years, career_prospects, description) 
            VALUES (2, 'Foundation in Arts', 'Foundation', 1, 
                    'Pathway to Bachelor programs in Arts, Social Science, Business, and Management', 
                    'A comprehensive foundation program designed to prepare students for undergraduate studies in arts, social sciences, business, and management fields. Covers essential subjects including English, Mathematics, Business Studies, and Social Sciences.')
        """)
        conn.commit()
        print("✓ Added Foundation in Arts")
    except Exception as e:
        print(f"✗ Error: {e}")
else:
    print("\n✓ Foundation in Arts already exists")

# Add Foundation in Science
cursor.execute("SELECT program_id FROM PROGRAM WHERE program_name = 'Foundation in Science'")
if not cursor.fetchone():
    print("\n➕ Adding Foundation in Science...")
    try:
        cursor.execute("""
            INSERT INTO PROGRAM (faculty_id, program_name, level, duration_years, career_prospects, description) 
            VALUES (5, 'Foundation in Science', 'Foundation', 1, 
                    'Pathway to Bachelor programs in Science, Engineering, and Technology', 
                    'A comprehensive foundation program designed to prepare students for undergraduate studies in science, engineering, and technology fields. Covers essential subjects including Mathematics, Physics, Chemistry, and Biology.')
        """)
        conn.commit()
        print("✓ Added Foundation in Science")
    except Exception as e:
        print(f"✗ Error: {e}")
else:
    print("\n✓ Foundation in Science already exists")

# Final verification
cursor.execute("""
    SELECT p.program_id, p.program_name, p.level, f.faculty_name
    FROM PROGRAM p
    JOIN FACULTY f ON p.faculty_id = f.faculty_id
    WHERE p.level = 'Foundation'
    ORDER BY p.program_name
""")
final = cursor.fetchall()
print(f"\n{'='*50}")
print(f"Final Foundation Programs: {len(final)}")
for p in final:
    print(f"  ✓ {p['program_name']} (Faculty: {p['faculty_name']})")
print(f"{'='*50}")

cursor.close()
conn.close()
