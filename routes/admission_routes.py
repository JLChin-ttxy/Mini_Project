"""
Admission Routes - Main admission pages and procedures
"""
from flask import Blueprint, render_template, request, jsonify, session
from utils.db_helper import get_db_connection
from utils.eligibility_checker import EligibilityChecker
from utils.document_generator import DocumentChecklistGenerator
from utils.deadline_tracker import DeadlineTracker
from flask import send_file
from datetime import datetime
import io

# Try to import email sender
try:
    from utils.email_sender import send_deadline_reminder, check_and_send_reminders, send_email
    HAS_EMAIL_SENDER = True
except ImportError:
    HAS_EMAIL_SENDER = False
    print("Warning: Email sender not available. Email notifications will be disabled.")

# Try to import ApplicationFormGenerator, but don't fail if reportlab isn't installed
try:
    from utils.application_form_generator import ApplicationFormGenerator
    HAS_PDF_GENERATOR = True
except ImportError:
    HAS_PDF_GENERATOR = False
    print("Warning: reportlab not installed. PDF form generation will be disabled.")

bp = Blueprint('admission', __name__, url_prefix='/admission')

@bp.route('/')
def admission_home():
    """Admission module home page"""
    conn = get_db_connection()
    if not conn:
        return render_template('error.html', message="Database connection failed"), 500
    
    try:
        cursor = conn.cursor(dictionary=True)
        
        # Get all programs grouped by level
        cursor.execute("""
            SELECT p.program_id, p.program_name, p.level, p.duration_years,
                   f.faculty_name, p.description
            FROM PROGRAM p
            JOIN FACULTY f ON p.faculty_id = f.faculty_id
            ORDER BY 
                CASE p.level
                    WHEN 'Foundation' THEN 1
                    WHEN 'Diploma' THEN 2
                    WHEN 'Bachelor' THEN 3
                    WHEN 'Master' THEN 4
                    WHEN 'PhD' THEN 5
                    ELSE 6
                END,
                f.faculty_name, 
                p.program_name
        """)
        all_programs = cursor.fetchall()
        
        # Group programs by level
        programs_by_level = {
            'Foundation': [],
            'Diploma': [],
            'Bachelor': [],
            'Master': [],
            'PhD': []
        }
        
        for program in all_programs:
            level = program['level']
            # Debug: print levels found (can remove later)
            # print(f"Found program: {program['program_name']} with level: {level}")
            if level in programs_by_level:
                programs_by_level[level].append(program)
            # Also handle case where level might be stored differently
            elif level and level.lower() == 'foundation':
                programs_by_level['Foundation'].append(program)
        
        # Get upcoming deadlines
        cursor.execute("""
            SELECT event_type, start_date, end_date, id.description,
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
                             programs_by_level=programs_by_level, 
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
            
            # Sort requirements by priority order (like UTAR website)
            qualification_order = ['STPM', 'UEC', 'A-Level', 'SAM', 'Matriculation', 'Foundation', 'Diploma', 'SPM']
            requirements_list.sort(key=lambda x: (
                qualification_order.index(x['qualification_type']) 
                if x['qualification_type'] in qualification_order 
                else 999
            ))
            
            cursor.close()
            conn.close()
            
            return render_template('admission/requirements.html',
                                 program=program_info,
                                 requirements=requirements_list)
        else:
            # Get undergraduate programs (Bachelor, Diploma) grouped by faculty with requirements
            cursor.execute("""
                SELECT p.program_id, p.program_name, p.level, p.duration_years,
                       f.faculty_id, f.faculty_name,
                       ar.qualification_type, ar.minimum_grade, ar.additional_requirements
                FROM PROGRAM p
                JOIN FACULTY f ON p.faculty_id = f.faculty_id
                LEFT JOIN ADMISSION_REQUIREMENT ar ON p.program_id = ar.program_id
                WHERE p.level IN ('Bachelor', 'Diploma')
                ORDER BY f.faculty_name, p.program_name, ar.qualification_type
            """)
            undergrad_data = cursor.fetchall()
            
            # Get postgraduate programs (Master, PhD) grouped by faculty with requirements
            cursor.execute("""
                SELECT p.program_id, p.program_name, p.level, p.duration_years,
                       f.faculty_id, f.faculty_name,
                       ar.qualification_type, ar.minimum_grade, ar.additional_requirements
                FROM PROGRAM p
                JOIN FACULTY f ON p.faculty_id = f.faculty_id
                LEFT JOIN ADMISSION_REQUIREMENT ar ON p.program_id = ar.program_id
                WHERE p.level IN ('Master', 'PhD')
                ORDER BY f.faculty_name, p.program_name, ar.qualification_type
            """)
            postgrad_data = cursor.fetchall()
            
            # Get all Bachelor programs for foundation suggestions
            cursor.execute("""
                SELECT p.program_id, p.program_name, p.level, f.faculty_name
                FROM PROGRAM p
                JOIN FACULTY f ON p.faculty_id = f.faculty_id
                WHERE p.level = 'Bachelor'
                ORDER BY f.faculty_name, p.program_name
            """)
            bachelor_programs = cursor.fetchall()
            
            # Group undergraduate programs by faculty
            undergrad_faculties = {}
            for row in undergrad_data:
                faculty_id = row['faculty_id']
                if faculty_id not in undergrad_faculties:
                    undergrad_faculties[faculty_id] = {
                        'faculty_name': row['faculty_name'],
                        'programs': {}
                    }
                
                program_id = row['program_id']
                if program_id not in undergrad_faculties[faculty_id]['programs']:
                    undergrad_faculties[faculty_id]['programs'][program_id] = {
                        'program_name': row['program_name'],
                        'level': row['level'],
                        'duration_years': row['duration_years'],
                        'requirements': []
                    }
                
                if row['qualification_type']:
                    undergrad_faculties[faculty_id]['programs'][program_id]['requirements'].append({
                        'qualification_type': row['qualification_type'],
                        'minimum_grade': row['minimum_grade'],
                        'additional_requirements': row['additional_requirements']
                    })
            
            # Group postgraduate programs by faculty
            postgrad_faculties = {}
            for row in postgrad_data:
                faculty_id = row['faculty_id']
                if faculty_id not in postgrad_faculties:
                    postgrad_faculties[faculty_id] = {
                        'faculty_name': row['faculty_name'],
                        'programs': {}
                    }
                
                program_id = row['program_id']
                if program_id not in postgrad_faculties[faculty_id]['programs']:
                    postgrad_faculties[faculty_id]['programs'][program_id] = {
                        'program_name': row['program_name'],
                        'level': row['level'],
                        'duration_years': row['duration_years'],
                        'requirements': []
                    }
                
                if row['qualification_type']:
                    postgrad_faculties[faculty_id]['programs'][program_id]['requirements'].append({
                        'qualification_type': row['qualification_type'],
                        'minimum_grade': row['minimum_grade'],
                        'additional_requirements': row['additional_requirements']
                    })
            
            # Create Foundation programs data structure
            foundation_programs = {
                'science': {
                    'program_name': 'Foundation in Science',
                    'duration_years': 1,
                    'requirements': [],
                    'suggested_degrees': []
                },
                'arts': {
                    'program_name': 'Foundation in Arts',
                    'duration_years': 1,
                    'requirements': [],
                    'suggested_degrees': []
                }
            }
            
            # Categorize bachelor programs for suggestions
            science_keywords = ['science', 'engineering', 'computer', 'technology', 'mathematics', 'physics', 'chemistry', 'biology', 'medicine', 'pharmacy', 'architecture']
            arts_keywords = ['business', 'accounting', 'management', 'commerce', 'economics', 'arts', 'design', 'communication', 'media', 'law', 'education', 'psychology', 'social']
            
            for prog in bachelor_programs:
                prog_name_lower = prog['program_name'].lower()
                faculty_lower = prog['faculty_name'].lower()
                
                is_science = any(keyword in prog_name_lower or keyword in faculty_lower for keyword in science_keywords)
                is_arts = any(keyword in prog_name_lower or keyword in faculty_lower for keyword in arts_keywords)
                
                prog_info = {
                    'program_id': prog['program_id'],
                    'program_name': prog['program_name'],
                    'faculty_name': prog['faculty_name']
                }
                
                if is_science:
                    foundation_programs['science']['suggested_degrees'].append(prog_info)
                if is_arts:
                    foundation_programs['arts']['suggested_degrees'].append(prog_info)
            
            cursor.close()
            conn.close()
            
            return render_template('admission/requirements_list.html',
                                 undergrad_faculties=undergrad_faculties,
                                 postgrad_faculties=postgrad_faculties,
                                 foundation_programs=foundation_programs)
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

@bp.route('/application-form')
def application_form():
    """Online application form page"""
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
        
        return render_template('admission/application_form.html',
                             programs=programs)
    except Exception as e:
        if conn:
            conn.close()
        return render_template('error.html', message=str(e)), 500

@bp.route('/submit-application', methods=['POST'])
def submit_application():
    """Handle application form submission"""
    try:
        # Get form data
        form_data = request.form.to_dict()
        files = request.files
        
        # Here you would typically:
        # 1. Validate the form data
        # 2. Save uploaded files
        # 3. Store application in database
        # 4. Send confirmation email
        # 5. Generate application reference number
        
        # For now, return a success message
        return jsonify({
            'success': True,
            'message': 'Application submitted successfully!',
            'reference_number': 'APP' + datetime.now().strftime('%Y%m%d%H%M%S')
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error submitting application: {str(e)}'
        }), 500

@bp.route('/deadlines')
def deadlines():
    """Important dates and deadlines page with calendar view"""
    conn = get_db_connection()
    if not conn:
        return render_template('error.html', message="Database connection failed"), 500
    
    try:
        tracker = DeadlineTracker(conn)
        upcoming_dates = tracker.get_upcoming_dates()
        all_dates = tracker.get_all_dates()
        
        # Get all programs for email subscription
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT p.program_id, p.program_name, p.level, f.faculty_name
            FROM PROGRAM p
            JOIN FACULTY f ON p.faculty_id = f.faculty_id
            ORDER BY p.level, f.faculty_name, p.program_name
        """)
        programs = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return render_template('admission/deadlines_calendar.html',
                             upcoming_dates=upcoming_dates,
                             all_dates=all_dates,
                             programs=programs)
    except Exception as e:
        if conn:
            conn.close()
        return render_template('error.html', message=str(e)), 500

@bp.route('/subscribe-email', methods=['POST'])
def subscribe_email():
    """Subscribe user to email notifications for deadline reminders"""
    conn = get_db_connection()
    if not conn:
        return jsonify({'success': False, 'message': 'Database connection failed'}), 500
    
    try:
        data = request.get_json()
        email = data.get('email', '').strip()
        program_ids = data.get('program_ids', [])
        
        if not email or not program_ids:
            return jsonify({'success': False, 'message': 'Email and at least one program selection required'}), 400
        
        # Validate email format
        import re
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            return jsonify({'success': False, 'message': 'Invalid email format'}), 400
        
        cursor = conn.cursor(dictionary=True)
        
        # Insert or update subscriptions
        subscribed_programs = []
        for program_id in program_ids:
            try:
                cursor.execute("""
                    INSERT INTO EMAIL_NOTIFICATION 
                    (email, program_id, notification_type, days_before, is_active)
                    VALUES (%s, %s, 'Deadline Reminder', 14, TRUE)
                    ON DUPLICATE KEY UPDATE is_active = TRUE, subscribed_at = CURRENT_TIMESTAMP
                """, (email, program_id))
                subscribed_programs.append(program_id)
            except Exception as e:
                # If table doesn't exist yet, return helpful message
                if "doesn't exist" in str(e) or "Table" in str(e) and "doesn't exist" in str(e):
                    cursor.close()
                    conn.close()
                    return jsonify({
                        'success': False, 
                        'message': 'Email notification system not set up. Please run Database/email_notifications_migration.sql first.'
                    }), 500
                print(f"Warning: Error subscribing to program {program_id}: {e}")
                continue
        
        if subscribed_programs:
            # Get program names for confirmation email BEFORE closing connection
            program_names = []
            try:
                cursor.execute("""
                    SELECT program_name FROM PROGRAM 
                    WHERE program_id IN (%s)
                """ % ','.join(['%s'] * len(subscribed_programs)), subscribed_programs)
                program_names = [row['program_name'] for row in cursor.fetchall()]
            except Exception as e:
                print(f"Warning: Could not fetch program names: {e}")
            
        conn.commit()
        cursor.close()
        conn.close()
        
        if subscribed_programs:
            # Send confirmation email if email sender is available
            if HAS_EMAIL_SENDER:
                try:
                    # Send confirmation email
                    subject = "Email Subscription Confirmation - SKL University"
                    body_html = f"""
                    <html>
                      <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                        <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                          <h2 style="color: #1e3a8a;">Thank You for Subscribing!</h2>
                          <p>Dear Applicant,</p>
                          <p>You have successfully subscribed to email reminders for the following program(s):</p>
                          <ul>
                            {'<li>'.join([''] + program_names) if program_names else '<li>No programs selected</li>'}
                          </ul>
                          <p>You will receive email reminders <strong>14 days before</strong> application deadlines.</p>
                          <p>If you did not subscribe to this service, please ignore this email.</p>
                          <hr style="border: none; border-top: 1px solid #eee; margin: 20px 0;">
                          <p style="font-size: 0.9em; color: #666;">
                            Best regards,<br>
                            <strong>SKL University Admission Office</strong><br>
                            123, Jalan Bandar Timah, 31900 Kampar Perak.<br>
                            Phone: +60-3-1234-5678<br>
                            Email: SKL123@edu.my
                          </p>
                        </div>
                      </body>
                    </html>
                    """
                    send_email(email, subject, body_html)
                except Exception as e:
                    print(f"Warning: Could not send confirmation email: {e}")
            
            return jsonify({
                'success': True, 
                'message': f'Successfully subscribed to email reminders for {len(subscribed_programs)} program(s)!'
            }), 200
        else:
            return jsonify({'success': False, 'message': 'Failed to subscribe. Please try again.'}), 500
            
    except Exception as e:
        if conn:
            conn.close()
        return jsonify({'success': False, 'message': str(e)}), 500

@bp.route('/download-application-form')
def download_application_form():
    """Generate and download offline application form PDF"""
    if not HAS_PDF_GENERATOR:
        return render_template('error.html', 
                             message="PDF form generation is not available. Please install reportlab: pip install reportlab"), 503
    
    try:
        generator = ApplicationFormGenerator()
        pdf_buffer = generator.generate_form()
        
        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'SKL_Application_Form_{datetime.now().strftime("%Y%m%d")}.pdf'
        )
    except Exception as e:
        return render_template('error.html', message=f"Error generating form: {str(e)}"), 500

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

@bp.route('/send-email-reminders', methods=['POST'])
def send_email_reminders():
    """Manually trigger email reminder sending (for testing or scheduled tasks)"""
    if not HAS_EMAIL_SENDER:
        return jsonify({
            'success': False, 
            'message': 'Email sending is not configured. Please set up SMTP settings.'
        }), 503
    
    try:
        sent_count = check_and_send_reminders()
        return jsonify({
            'success': True,
            'message': f'Email reminder check completed. Sent {sent_count} reminder(s).'
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error sending reminders: {str(e)}'
        }), 500


