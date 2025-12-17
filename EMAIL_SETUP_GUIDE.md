# Email Notification Setup Guide

## Overview
The email notification system sends reminder emails to subscribers 14 days before application deadlines.

## Setup Instructions

### 1. Configure SMTP Settings

Create a `.env` file in your project root (or set environment variables):

```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
FROM_EMAIL=noreply@skl.edu.my
FROM_NAME=SKL University Admission Office
```

### 2. For Gmail Users

If using Gmail, you need to:
1. Enable 2-Factor Authentication on your Google account
2. Generate an "App Password":
   - Go to: https://myaccount.google.com/apppasswords
   - Create a new app password for "Mail"
   - Use this password (not your regular Gmail password) in `SMTP_PASSWORD`

### 3. For Other Email Providers

**Outlook/Hotmail:**
```env
SMTP_SERVER=smtp-mail.outlook.com
SMTP_PORT=587
```

**Yahoo:**
```env
SMTP_SERVER=smtp.mail.yahoo.com
SMTP_PORT=587
```

**Custom SMTP:**
Use your email provider's SMTP settings.

### 4. Install Required Packages

The email system uses Python's built-in `smtplib`, so no additional packages are needed.

### 5. Test Email Sending

You can test the email system by:
1. Subscribing to email reminders via the deadlines page
2. Manually triggering reminders (if you have admin access):
   ```python
   from utils.email_sender import check_and_send_reminders
   check_and_send_reminders()
   ```

### 6. Automated Reminder Sending

To automatically send reminders daily, you can:

**Option A: Use a cron job (Linux/Mac)**
```bash
# Add to crontab (runs daily at 9 AM)
0 9 * * * cd /path/to/project && python -c "from utils.email_sender import check_and_send_reminders; check_and_send_reminders()"
```

**Option B: Use Windows Task Scheduler**
- Create a scheduled task that runs daily
- Run: `python -c "from utils.email_sender import check_and_send_reminders; check_and_send_reminders()"`

**Option C: Use Flask-APScheduler (for production)**
Add to your `app.py`:
```python
from apscheduler.schedulers.background import BackgroundScheduler
from utils.email_sender import check_and_send_reminders

scheduler = BackgroundScheduler()
scheduler.add_job(func=check_and_send_reminders, trigger="cron", hour=9, minute=0)
scheduler.start()
```

## How It Works

1. **User Subscribes**: User enters email and selects programs on the deadlines page
2. **Subscription Stored**: Email and program selections are saved in `EMAIL_NOTIFICATION` table
3. **Reminder Check**: System checks daily for deadlines that are exactly 14 days away
4. **Email Sent**: Reminder email is sent to subscribed users
5. **Timestamp Updated**: `last_sent` field is updated to prevent duplicate emails

## Email Content

The reminder email includes:
- Program name
- Deadline date
- Days remaining
- Contact information
- Professional HTML formatting

## Troubleshooting

**Emails not sending:**
- Check SMTP credentials in `.env` file
- Verify firewall allows SMTP connections
- Check spam folder
- Review server logs for error messages

**"Email not configured" warning:**
- Make sure `.env` file exists with SMTP settings
- Or set environment variables directly

**Duplicate emails:**
- The system prevents duplicates by checking `last_sent` timestamp
- Each subscription sends only one reminder per deadline
