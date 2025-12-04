# SKL University - Quick Setup Guide

## Quick Start

### 1. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 2. Setup MySQL Database

**IMPORTANT: Make sure MySQL is running before proceeding!**

**Step 1: Check if MySQL is running**
- **Windows**: Open Services (Win+R → type `services.msc` → Enter), find "MySQL" service and make sure it's "Running"
- Or open Command Prompt as Administrator and run: `net start MySQL`

**Step 2: Test Database Connection**
Run the diagnostic script:
```bash
python test_db_connection.py
```
This will tell you:
- If MySQL server is running
- If the database exists
- If connection works
- What tables are available

**Step 3: Create Database and Tables**

**Option A: Using MySQL Command Line**
```bash
# Connect to MySQL (if you have a password, use: mysql -u root -p)
mysql -u root

# Then run these commands:
source Database/schema.sql
source Database/data.sql
exit
```

**Option B: Using MySQL Workbench**
- Open MySQL Workbench
- Connect to your MySQL server (localhost, user: root, password: your password or empty)
- Click "File" → "Open SQL Script"
- Open `Database/schema.sql` and click the Execute button (⚡)
- Open `Database/data.sql` and click the Execute button (⚡)

**Option C: Using Command Line (Windows PowerShell)**
```powershell
# If MySQL is in your PATH:
mysql -u root -e "source Database/schema.sql"
mysql -u root -e "source Database/data.sql"

# Or if you need to specify full path:
& "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -u root < Database\schema.sql
& "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -u root < Database\data.sql
```

### 3. Configure Database Connection

Edit these files and update the database password:

**File: `app.py` (around line 20)**
```python
DB_CONFIG = {
    'host': 'localhost',
    'database': 'university_admission_db',
    'user': 'root',
    'password': 'YOUR_PASSWORD_HERE',  # Change this
    ...
}
```

**File: `utils/db_helper.py` (around line 8)**
```python
DB_CONFIG = {
    'host': 'localhost',
    'database': 'university_admission_db',
    'user': 'root',
    'password': 'YOUR_PASSWORD_HERE',  # Change this
    ...
}
```

### 4. Copy Logo File

Copy the logo from Website folder to static folder:
```bash
# Windows PowerShell
Copy-Item "Website\SKL logo.png" -Destination "static\images\SKL logo.png"

# Or manually copy the file
```

### 5. Run the Application

```bash
python app.py
```

### 6. Access the Website

Open your browser and go to:
```
http://localhost:5000
```

## Testing the Features

### Test Eligibility Checker
1. Go to: http://localhost:5000/admission/check-eligibility
2. Select a program
3. Enter qualification (e.g., STPM)
4. Enter CGPA (e.g., 3.50)
5. Click "Check Eligibility"

### Test Document Checklist
1. Go to: http://localhost:5000/admission/document-checklist
2. Select a program
3. Choose country (Malaysia or International)
4. Click "Generate Checklist"

### Test Deadlines
1. Go to: http://localhost:5000/admission/deadlines
2. View upcoming deadlines with urgency indicators

### Test Chatbot
1. Click the chat button (bottom right)
2. Ask questions like:
   - "What are the admission requirements?"
   - "How do I apply?"
   - "What are the deadlines?"
   - "What documents do I need?"

## Common Issues

### Database Connection Error ("Database connection failed")

**First, run the diagnostic script:**
```bash
python test_db_connection.py
```

**Common fixes:**

1. **MySQL is not running**
   - Windows: Open Services → Find "MySQL" → Right-click → Start
   - Or run: `net start MySQL` (as Administrator)

2. **Database doesn't exist**
   - Run: `python test_db_connection.py` - it will try to create it
   - Or manually: `mysql -u root -e "CREATE DATABASE university_admission_db;"`

3. **Wrong password**
   - If you set a MySQL password, update it in:
     - `app.py` (line 23)
     - `utils/db_helper.py` (line 12)
   - If you don't have a password, make sure it's set to `''` (empty string)

4. **Tables don't exist**
   - Run `Database/schema.sql` to create tables
   - Run `Database/data.sql` to insert sample data

5. **MySQL not installed**
   - Download MySQL from: https://dev.mysql.com/downloads/installer/
   - Or use XAMPP which includes MySQL: https://www.apachefriends.org/

### Module Not Found Error
- Activate virtual environment
- Run `pip install -r requirements.txt` again

### Static Files Not Loading
- Check that files are in `static/` folder
- Clear browser cache
- Check file paths in templates

### Logo Not Showing
- Ensure `SKL logo.png` is in `static/images/` folder
- Check file name matches exactly (case-sensitive)

## Next Steps

1. **Customize Content**: Update program information in database
2. **Add More Programs**: Insert more programs using the database
3. **Configure Email**: Set up email notifications (future feature)
4. **Deploy**: Use a production server like Gunicorn for deployment

## Support

If you encounter issues:
1. Check the error message in the terminal
2. Verify database connection
3. Ensure all dependencies are installed
4. Check file paths and permissions

---

**Note**: This is a development setup. For production, use a proper WSGI server and configure security settings.


