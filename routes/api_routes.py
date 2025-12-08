"""
API Routes - RESTful endpoints for admission module
"""
from flask import Blueprint, request, jsonify
from utils.db_helper import get_db_connection
from utils.eligibility_checker import EligibilityChecker
from utils.document_generator import DocumentChecklistGenerator
from utils.deadline_tracker import DeadlineTracker
import json

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/check-eligibility', methods=['POST'])
def api_check_eligibility():
    """API endpoint for eligibility checking"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        program_id = data.get('program_id')
        qualification = data.get('qualification')
        grades = data.get('grades', {})
        additional_info = data.get('additional_info', {})
        
        if not program_id or not qualification:
            return jsonify({'error': 'Missing required fields'}), 400
        
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        checker = EligibilityChecker(conn)
        result = checker.check_eligibility(
            program_id=program_id,
            qualification=qualification,
            grades=grades,
            additional_info=additional_info
        )
        
        conn.close()
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/document-checklist', methods=['GET', 'POST'])
def api_document_checklist():
    """API endpoint for document checklist generation"""
    try:
        if request.method == 'GET':
            program_id = request.args.get('program_id', type=int)
            country = request.args.get('country', 'Malaysia')
        else:
            data = request.get_json()
            program_id = data.get('program_id')
            country = data.get('country', 'Malaysia')
        
        if not program_id:
            return jsonify({'error': 'Program ID is required'}), 400
        
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        generator = DocumentChecklistGenerator(conn)
        checklist = generator.generate_checklist(program_id, country)
        program_info = generator.get_program_info(program_id)
        
        conn.close()
        
        return jsonify({
            'program': program_info,
            'checklist': checklist,
            'country': country
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/deadlines', methods=['GET'])
def api_deadlines():
    """API endpoint for deadline information"""
    try:
        program_id = request.args.get('program_id', type=int)
        days_ahead = request.args.get('days', type=int, default=90)
        
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        tracker = DeadlineTracker(conn)
        
        if program_id:
            dates = tracker.get_program_dates(program_id, days_ahead)
        else:
            dates = tracker.get_upcoming_dates(days_ahead)
        
        conn.close()
        
        return jsonify({
            'deadlines': dates,
            'count': len(dates)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/programs', methods=['GET'])
def api_programs():
    """API endpoint to get all programs"""
    try:
        faculty_id = request.args.get('faculty_id', type=int)
        level = request.args.get('level')
        
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = conn.cursor(dictionary=True)
        
        query = """
            SELECT p.program_id, p.program_name, p.level, p.duration_years,
                   p.description, p.career_prospects,
                   f.faculty_id, f.faculty_name
            FROM PROGRAM p
            JOIN FACULTY f ON p.faculty_id = f.faculty_id
            WHERE 1=1
        """
        params = []
        
        if faculty_id:
            query += " AND f.faculty_id = %s"
            params.append(faculty_id)
        
        if level:
            query += " AND p.level = %s"
            params.append(level)
        
        query += " ORDER BY f.faculty_name, p.program_name"
        
        cursor.execute(query, params)
        programs = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'programs': programs,
            'count': len(programs)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/qualifications', methods=['GET'])
def api_qualifications():
    """API endpoint to get available qualification types"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT qualification_type
            FROM ADMISSION_REQUIREMENT
            ORDER BY qualification_type
        """)
        qualifications = [row[0] for row in cursor.fetchall()]
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'qualifications': qualifications
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


