# SKL University - Admission Requirements & Application Procedure Module

A comprehensive Flask-based web application for university admission management with AI-powered features.

## Features

### Core Innovations

1. **AI-Driven Eligibility Checking**
   - NLP-like matching of user qualifications against program requirements
   - Automatic qualification equivalency detection
   - Real-time eligibility feedback with confidence scores

2. **Step-by-Step Application Guidelines**
   - Interactive online and offline application procedures
   - Clear, user-friendly step-by-step instructions
   - Support for both Malaysian and international applicants

3. **Real-Time Deadline Tracking**
   - Visual urgency indicators (critical, high, medium, low)
   - Days remaining calculations
   - Program-specific deadline filtering

4. **Customized Document Checklists**
   - Program-specific document requirements
   - Country-based customization (Malaysia vs International)
   - EMGS and UPU integration for international and local students

5. **Enhanced Chatbot Interface**
   - Intent detection for admission queries
   - Context-aware responses
   - Multi-language support ready

## Technology Stack

- **Backend**: Flask (Python)
- **Database**: MySQL
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **AI/NLP**: Custom intent detection and matching algorithms

## Installation

### Prerequisites

- Python 3.8 or higher
- MySQL 5.7 or higher
- pip (Python package manager)

### Setup Steps

1. **Clone or navigate to the project directory**
   ```bash
   cd Mini_Project
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Database Setup**
   - Create MySQL database using the schema file:
     ```bash
     mysql -u root -p < Database/schema.sql
     ```
   - Populate with sample data:
     ```bash
     mysql -u root -p < Database/data.sql
     ```

5. **Configure Database Connection**
   - Edit `app.py` and `utils/db_helper.py`
   - Update the `DB_CONFIG` dictionary with your MySQL credentials:
     ```python
     DB_CONFIG = {
         'host': 'localhost',
         'database': 'university_admission_db',
         'user': 'root',
         'password': 'your_password',  # Update this
         'charset': 'utf8mb4',
         'collation': 'utf8mb4_unicode_ci'
     }
     ```

6. **Copy Static Files**
   - Copy `Website/SKL logo.png` to `static/images/SKL logo.png`
   - Ensure all static files are in place

7. **Run the Application**
   ```bash
   python app.py
   ```

8. **Access the Application**
   - Open your browser and navigate to: `http://localhost:5000`

## Project Structure

```
Mini_Project/
├── app.py                 # Main Flask application
├── routes/                # Route blueprints
│   ├── admission_routes.py
│   ├── api_routes.py
│   └── chatbot_routes.py
├── utils/                 # Utility modules
│   ├── db_helper.py
│   ├── eligibility_checker.py
│   ├── document_generator.py
│   ├── deadline_tracker.py
│   └── chatbot_handler.py
├── templates/             # Jinja2 templates
│   ├── base.html
│   ├── main.html
│   └── admission/
│       ├── home.html
│       ├── check_eligibility.html
│       ├── application_procedure.html
│       ├── deadlines.html
│       ├── document_checklist.html
│       └── requirements.html
├── static/                # Static files
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   ├── main.js
│   │   └── script.js
│   └── images/
│       └── SKL logo.png
├── Database/              # Database files
│   ├── schema.sql
│   └── data.sql
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## API Endpoints

### Admission APIs

- `GET /admission/` - Admission home page
- `GET /admission/requirements` - View admission requirements
- `GET /admission/check-eligibility` - Eligibility checking page
- `GET /admission/application-procedure` - Application procedure guide
- `GET /admission/deadlines` - Important dates and deadlines
- `GET /admission/document-checklist` - Document checklist generator

### REST APIs

- `POST /api/check-eligibility` - Check eligibility (JSON)
- `GET /api/document-checklist` - Get document checklist (JSON)
- `GET /api/deadlines` - Get deadline information (JSON)
- `GET /api/programs` - Get all programs (JSON)
- `GET /api/qualifications` - Get qualification types (JSON)

### Chatbot APIs

- `POST /chatbot/message` - Send message to chatbot
- `GET /chatbot/session` - Get or create session
- `GET /chatbot/history` - Get chat history

## Key Features Implementation

### 1. Eligibility Checking
The system uses pattern matching and keyword extraction to match user qualifications against program requirements stored in the database.

### 2. Document Checklist
Generates personalized checklists based on:
- Selected program
- Applicant's country (Malaysia/International)
- Program-specific requirements
- EMGS requirements for international students

### 3. Deadline Tracking
- Calculates urgency levels automatically
- Shows days remaining
- Filters by program and date range

### 4. Chatbot
- Intent detection using pattern matching
- Context-aware responses
- Saves conversation history

## Configuration

### Database Configuration
Update database credentials in:
- `app.py` (line ~20)
- `utils/db_helper.py` (line ~8)

### Secret Key
Change the secret key in `app.py` for production:
```python
app.secret_key = 'your-secret-key-here'
```

## Troubleshooting

### Database Connection Issues
- Ensure MySQL is running
- Verify database credentials
- Check if database `university_admission_db` exists
- Ensure all tables are created (run schema.sql)

### Static Files Not Loading
- Verify file paths in templates use `url_for('static', ...)`
- Check that static files are in the `static/` directory
- Clear browser cache

### Import Errors
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt` again
- Check Python version (3.8+)

## Future Enhancements

- Integration with Dialogflow for advanced NLP
- Email notification system for deadlines
- Online application form submission
- File upload functionality
- Multi-language support (Malay, Chinese, Tamil)
- Admin dashboard for managing admissions

## License

This project is developed for SKL University admission system.

## Support

For issues or questions, please contact the development team.

---

**Note**: This is a development version. For production deployment, ensure:
- Secure secret key
- Database connection security
- HTTPS enabled
- Error logging configured
- Production-grade WSGI server (e.g., Gunicorn)


