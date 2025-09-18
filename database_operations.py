from database import get_db_connection

# Insert data into the database (dynamic input)
def insert_report(patient_id, report_text, summary, category, prediction):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO reports (patient_id, report_text, summary, category, prediction)
        VALUES (?, ?, ?, ?, ?)
    ''', (patient_id, report_text, summary, category, prediction))
    conn.commit()
    conn.close()

# Update report data in the database
def update_report(report_id, new_report_text, new_summary, new_category, new_prediction):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE reports
        SET report_text = ?, summary = ?, category = ?, prediction = ?
        WHERE report_id = ?
    ''', (new_report_text, new_summary, new_category, new_prediction, report_id))
    conn.commit()
    conn.close()

# Delete a report based on report_id
def delete_report(report_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        DELETE FROM reports WHERE report_id = ?
    ''', (report_id,))
    conn.commit()
    conn.close()

# Search reports by category
def search_reports_by_category(category):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM reports WHERE category = ?
    ''', (category,))
    results = cursor.fetchall()
    conn.close()
    
    for report in results:
        print(report)
