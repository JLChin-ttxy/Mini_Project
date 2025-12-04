"""
Admission Routes - Main admission pages and procedures
"""
from flask import Blueprint, render_template, request, jsonify, session
from utils.db_helper import get_db_connection
from utils.eligibility_checker import EligibilityChecker
from utils.document_generator import DocumentChecklistGenerator
from utils.deadline_tracker import DeadlineTracker
from datetime import datetime

bp = Blueprint('admission', __name__, url_prefix='/admission')

@bp.route('/')
def admission_home():
    """Admission module home page"""
    conn = get_db_connection()
    if not conn:
        return render_template('error.html', message="Database connection failed"), 500
    
    try:
        cursor = conn.cursor(dictionary=True)
        
        # Get all programs
        cursor.execute("""
            SELECT p.program_id, p.program_name, p.level, p.duration_years,
                   f.faculty_name, p.description
            FROM PROGRAM p
            JOIN FACULTY f ON p.faculty_id = f.faculty_id
            ORDER BY f.faculty_name, p.program_name
        """)
        programs = cursor.fetchall()
        
        # Get upcoming deadlines
        cursor.execute("""
            SELECT event_type, start_date, end_date, description,
                   p.program_name, p.program_id
            FROM IMPORTANT_DATE id
            JOIN PROGRAM p ON id.program_id = p.program_id
            WHERE end_date >= CURDATE()
            ORDER BY start_date ASC
            LIMIT 10
        """)
        deadlines = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return render_template('admission/home.html', 
                             programs=programs, 
                             deadlines=deadlines)
    except Exception as e:
        if conn:
            conn.close()
        return render_template('error.html', message=str(e)), 500

@bp.route('/requirements')
def requirements():
    """Admission requirements page"""
    program_id = request.args.get('program_id', type=int)
    
    conn = get_db_connection()
    if not conn:
        return render_template('error.html', message="Database connection failed"), 500
    
    try:
        cursor = conn.cursor(dictionary=True)
        
        if program_id:
            # Get specific program requirements
            cursor.execute("""
                SELECT p.program_id, p.program_name, p.level, p.duration_years,
                       f.faculty_name, p.description,
                       ar.requirement_id, ar.qualification_type, ar.minimum_grade,
                       ar.additional_requirements, ar.entrance_exam_info
                FROM PROGRAM p
                JOIN FACULTY f ON p.faculty_id = f.faculty_id
                LEFT JOIN ADMISSION_REQUIREMENT ar ON p.program_id = ar.program_id
                WHERE p.program_id = %s
            """, (program_id,))
            requirements = cursor.fetchall()
            
            if not requirements:
                return render_template('error.html', message="Program not found"), 404
            
            program_info = requirements[0]
            requirements_list = [r for r in requirements if r['requirement_id']]
            
            cursor.close()
            conn.close()
            
            return render_template('admission/requirements.html',
                                 program=program_info,
                                 requirements=requirements_list)
        else:
            # Get all programs with requirements
            cursor.execute("""
                SELECT DISTINCT p.program_id, p.program_name, p.level,
                       f.faculty_name
                FROM PROGRAM p
                JOIN FACULTY f ON p.faculty_id = f.faculty_id
                LEFT JOIN ADMISSION_REQUIREMENT ar ON p.program_id = ar.program_id
                ORDER BY f.faculty_name, p.program_name
            """)
            programs = cursor.fetchall()
            
            cursor.close()
            conn.close()
            
            return render_template('admission/requirements_list.html',
                                 programs=programs)
    except Exception as e:
        if conn:
            conn.close()
        return render_template('error.html', message=str(e)), 500

@bp.route('/check-eligibility')
def check_eligibility():
    """Eligibility checking page"""
    return render_template('admission/check_eligibility.html')

@bp.route('/application-procedure')
def application_procedure():
    """Application procedure page"""
    procedure_type = request.args.get('type', 'online')  # online or offline
    
    conn = get_db_connection()
    if not conn:
        return render_template('error.html', message="Database connection failed"), 500
    
    try:
        cursor = conn.cursor(dictionary=True)
        
        # Get all programs for selection
        cursor.execute("""
            SELECT p.program_id, p.program_name, p.level,
                   f.faculty_name
            FROM PROGRAM p
            JOIN FACULTY f ON p.faculty_id = f.faculty_id
            ORDER BY f.faculty_name, p.program_name
        """)
        programs = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return render_template('admission/application_procedure.html',
                             procedure_type=procedure_type,
                             programs=programs)
    except Exception as e:
        if conn:
            conn.close()
        return render_template('error.html', message=str(e)), 500

@bp.route('/deadlines')
def deadlines():
    """Important dates and deadlines page"""
    conn = get_db_connection()
    if not conn:
        return render_template('error.html', message="Database connection failed"), 500
    
    try:
        tracker = DeadlineTracker(conn)
        upcoming_dates = tracker.get_upcoming_dates()
        all_dates = tracker.get_all_dates()
        
        conn.close()
        
        return render_template('admission/deadlines.html',
                             upcoming_dates=upcoming_dates,
                             all_dates=all_dates)
    except Exception as e:
        if conn:
            conn.close()
        return render_template('error.html', message=str(e)), 500

@bp.route('/document-checklist')
def document_checklist():
    """Document checklist page"""
    program_id = request.args.get('program_id', type=int)
    country = request.args.get('country', 'Malaysia')
    
    conn = get_db_connection()
    if not conn:
        return render_template('error.html', message="Database connection failed"), 500
    
    try:
        generator = DocumentChecklistGenerator(conn)
        
        if program_id:
            checklist = generator.generate_checklist(program_id, country)
            program_info = generator.get_program_info(program_id)
            
            conn.close()
            
            return render_template('admission/document_checklist.html',
                                 checklist=checklist,
                                 program=program_info,
                                 country=country)
        else:
            # Get all programs for selection
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT p.program_id, p.program_name, p.level,
                       f.faculty_name
                FROM PROGRAM p
                JOIN FACULTY f ON p.faculty_id = f.faculty_id
                ORDER BY f.faculty_name, p.program_name
            """)
            programs = cursor.fetchall()
            cursor.close()
            conn.close()
            
            return render_template('admission/document_checklist_select.html',
                                 programs=programs)
    except Exception as e:
        if conn:
            conn.close()
        return render_template('error.html', message=str(e)), 500


