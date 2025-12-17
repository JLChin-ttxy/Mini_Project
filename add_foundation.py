#!/usr/bin/env python3
"""Quick script to add Foundation programs - Run: python add_foundation.py"""
import sys
sys.path.insert(0, '.')
from utils.db_helper import get_db_connection

conn = get_db_connection()
if not conn:
    print("ERROR: Database connection failed")
    sys.exit(1)

cursor = conn.cursor()

# Update ENUM
try:
    cursor.execute("ALTER TABLE PROGRAM MODIFY COLUMN level ENUM('Foundation', 'Diploma', 'Bachelor', 'Master', 'PhD') NOT NULL")
    conn.commit()
    print("✓ ENUM updated")
except:
    pass

# Add Foundation in Arts
cursor.execute("SELECT program_id FROM PROGRAM WHERE program_name = 'Foundation in Arts'")
if not cursor.fetchone():
    cursor.execute("""
        INSERT INTO PROGRAM (faculty_id, program_name, level, duration_years, career_prospects, description) 
        VALUES (2, 'Foundation in Arts', 'Foundation', 1, 
                'Pathway to Bachelor programs', 
                'Foundation program for arts, social sciences, business, and management fields.')
    """)
    conn.commit()
    print("✓ Added Foundation in Arts")

# Add Foundation in Science
cursor.execute("SELECT program_id FROM PROGRAM WHERE program_name = 'Foundation in Science'")
if not cursor.fetchone():
    cursor.execute("""
        INSERT INTO PROGRAM (faculty_id, program_name, level, duration_years, career_prospects, description) 
        VALUES (5, 'Foundation in Science', 'Foundation', 1, 
                'Pathway to Bachelor programs', 
                'Foundation program for science, engineering, and technology fields.')
    """)
    conn.commit()
    print("✓ Added Foundation in Science")

# Verify
cursor.execute("SELECT program_id, program_name FROM PROGRAM WHERE level = 'Foundation'")
results = cursor.fetchall()
print(f"\n✓ Found {len(results)} Foundation program(s)")
for r in results:
    print(f"  - {r[1]}")

cursor.close()
conn.close()
print("\nDone! Refresh the admission page to see Foundation programs.")
