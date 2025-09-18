import sqlite3

# Function to get a connection to the database
def get_db_connection():
    conn = sqlite3.connect('medical_reports.db')
    return conn

# Function to create the database and table
def create_database():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reports (
            report_id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER,
            report_text TEXT,
            summary TEXT,
            category TEXT,
            prediction TEXT
        )
    ''')
    conn.commit()
    conn.close()
