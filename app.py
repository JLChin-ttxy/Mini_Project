"""
SKL University - Admission Requirements & Application Procedure Module
Flask Application Main Entry Point
"""
from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
from datetime import datetime, timedelta
import re
import json
from functools import wraps

app = Flask(__name__)
app.secret_key = 'skl-university-secret-key-2025'  # Change in production
CORS(app)

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'database': 'university_admission_db',
    'user': 'root',
    'password': '123456',  # MySQL root password
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_unicode_ci'
}

def get_db_connection():
    """Create and return database connection"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

# Import routes
try:
    from routes import admission_routes, chatbot_routes, api_routes, dialogflow_webhook
    
    # Register blueprints
    app.register_blueprint(admission_routes.bp)
    app.register_blueprint(chatbot_routes.bp)
    app.register_blueprint(api_routes.bp)
    app.register_blueprint(dialogflow_webhook.bp)
    print("✓ All blueprints registered successfully")
except ImportError as e:
    print(f"✗ ERROR: Could not import routes: {e}")
    import traceback
    traceback.print_exc()
except Exception as e:
    print(f"✗ ERROR: Failed to register blueprints: {e}")
    import traceback
    traceback.print_exc()

@app.route('/')
def index():
    """Home page - redirect to campus life page"""
    return render_template('main.html')

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

