"""
Email Sender - Send notification emails for deadline reminders
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
import os
from utils.db_helper import get_db_connection

# Email configuration - can be set via environment variables
SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
SMTP_USERNAME = os.getenv('SMTP_USERNAME', '')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD', '')
FROM_EMAIL = os.getenv('FROM_EMAIL', 'noreply@skl.edu.my')
FROM_NAME = os.getenv('FROM_NAME', 'SKL University Admission Office')


def send_email(to_email, subject, body_html, body_text=None):
    """
    Send an email using SMTP
    
    Args:
        to_email: Recipient email address
        subject: Email subject
        body_html: HTML email body
        body_text: Plain text email body (optional)
    
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    if not SMTP_USERNAME or not SMTP_PASSWORD:
        print(f"Warning: Email not configured. Would send to {to_email}: {subject}")
        return False
    
    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['From'] = f"{FROM_NAME} <{FROM_EMAIL}>"
        msg['To'] = to_email
        msg['Subject'] = subject
        
        # Add both plain text and HTML versions
        if body_text:
            part1 = MIMEText(body_text, 'plain')
            msg.attach(part1)
        
        part2 = MIMEText(body_html, 'html')
        msg.attach(part2)
        
        # Send email
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        print(f"Email sent successfully to {to_email}")
        return True
        
    except Exception as e:
        print(f"Error sending email to {to_email}: {e}")
        return False


def send_deadline_reminder(email, program_name, deadline_date, days_before=14):
    """
    Send a deadline reminder email
    
    Args:
        email: Recipient email
        program_name: Name of the program
        deadline_date: Deadline date (datetime or date object)
        days_before: Number of days before deadline to send reminder
    """
    if isinstance(deadline_date, str):
        deadline_date = datetime.strptime(deadline_date, '%Y-%m-%d').date()
    elif isinstance(deadline_date, datetime):
        deadline_date = deadline_date.date()
    
    subject = f"Reminder: Application Deadline for {program_name} - {days_before} Days Remaining"
    
    deadline_str = deadline_date.strftime('%d %B %Y')
    
    body_html = f"""
    <html>
      <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
          <h2 style="color: #1e3a8a;">Application Deadline Reminder</h2>
          <p>Dear Applicant,</p>
          <p>This is a reminder that the application deadline for <strong>{program_name}</strong> is approaching.</p>
          <div style="background: #f97316; color: white; padding: 15px; border-radius: 5px; margin: 20px 0;">
            <strong>Deadline: {deadline_str}</strong><br>
            <small>Only {days_before} days remaining!</small>
          </div>
          <p>Please ensure you have submitted your application and all required documents before this date.</p>
          <p>If you have already submitted your application, please disregard this reminder.</p>
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
    
    body_text = f"""
    Application Deadline Reminder
    
    Dear Applicant,
    
    This is a reminder that the application deadline for {program_name} is approaching.
    
    Deadline: {deadline_str}
    Only {days_before} days remaining!
    
    Please ensure you have submitted your application and all required documents before this date.
    
    Best regards,
    SKL University Admission Office
    """
    
    return send_email(email, subject, body_html, body_text)


def check_and_send_reminders():
    """
    Check for upcoming deadlines and send reminder emails to subscribed users
    This should be called periodically (e.g., daily via cron job or scheduler)
    """
    conn = get_db_connection()
    if not conn:
        print("Error: Could not connect to database for email reminders")
        return
    
    try:
        cursor = conn.cursor(dictionary=True)
        
        # Get all active subscriptions with upcoming deadlines
        today = datetime.now().date()
        
        cursor.execute("""
            SELECT en.email, en.days_before, en.program_id,
                   p.program_name, id.start_date, id.end_date, id.event_type
            FROM EMAIL_NOTIFICATION en
            JOIN PROGRAM p ON en.program_id = p.program_id
            LEFT JOIN IMPORTANT_DATE id ON p.program_id = id.program_id
            WHERE en.is_active = TRUE
              AND en.notification_type = 'Deadline Reminder'
              AND (id.end_date IS NOT NULL AND id.end_date >= CURDATE())
            ORDER BY en.email, id.end_date
        """)
        
        subscriptions = cursor.fetchall()
        
        sent_count = 0
        for sub in subscriptions:
            email = sub['email']
            program_name = sub['program_name']
            days_before = sub['days_before']
            deadline_date = sub['end_date']
            
            if not deadline_date:
                continue
            
            # Calculate days until deadline
            days_until = (deadline_date - today).days
            
            # Send reminder if it's exactly 'days_before' days before deadline
            if days_until == days_before:
                # Check if we already sent a reminder for this deadline
                cursor.execute("""
                    SELECT last_sent FROM EMAIL_NOTIFICATION
                    WHERE email = %s AND program_id = %s
                """, (email, sub['program_id']))
                
                last_sent = cursor.fetchone()
                if last_sent and last_sent['last_sent']:
                    last_sent_date = last_sent['last_sent'].date() if isinstance(last_sent['last_sent'], datetime) else last_sent['last_sent']
                    if last_sent_date == today:
                        continue  # Already sent today
                
                # Send the reminder
                if send_deadline_reminder(email, program_name, deadline_date, days_before):
                    # Update last_sent timestamp
                    cursor.execute("""
                        UPDATE EMAIL_NOTIFICATION
                        SET last_sent = CURRENT_TIMESTAMP
                        WHERE email = %s AND program_id = %s
                    """, (email, sub['program_id']))
                    conn.commit()
                    sent_count += 1
        
        cursor.close()
        conn.close()
        
        print(f"Email reminder check completed. Sent {sent_count} reminder(s).")
        return sent_count
        
    except Exception as e:
        print(f"Error checking reminders: {e}")
        if conn:
            conn.close()
        return 0
