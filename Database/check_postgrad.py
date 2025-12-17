"""
Quick script to check if postgraduate programs exist in the database
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.db_helper import get_db_connection

conn = get_db_connection()
if not conn:
    print("ERROR: Could not connect to database")
    sys.exit(1)

cursor = conn.cursor(dictionary=True)

# Check for Master's programs
cursor.execute("SELECT COUNT(*) as count FROM PROGRAM WHERE level = 'Master'")
master_count = cursor.fetchone()['count']

# Check for PhD programs
cursor.execute("SELECT COUNT(*) as count FROM PROGRAM WHERE level = 'PhD'")
phd_count = cursor.fetchone()['count']

print(f"Master's programs in database: {master_count}")
print(f"PhD programs in database: {phd_count}")

if master_count == 0 and phd_count == 0:
    print("\n❌ No postgraduate programs found!")
    print("Please run: python Database/add_postgrad_programs.py")
else:
    print("\n✅ Postgraduate programs found!")
    cursor.execute("""
        SELECT p.program_id, p.program_name, p.level, f.faculty_name
        FROM PROGRAM p
        JOIN FACULTY f ON p.faculty_id = f.faculty_id
        WHERE p.level IN ('Master', 'PhD')
        ORDER BY p.level, f.faculty_name
    """)
    programs = cursor.fetchall()
    print("\nPrograms:")
    for p in programs:
        print(f"  - [{p['level']}] {p['program_name']} ({p['faculty_name']})")

cursor.close()
conn.close()
