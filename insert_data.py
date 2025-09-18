from database import get_db_connection

def insert_report(patient_id, report_text, summary, category, prediction):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO reports (patient_id, report_text, summary, category, prediction)
        VALUES (?, ?, ?, ?, ?)
    ''', (patient_id, report_text, summary, category, prediction))
    conn.commit()
    conn.close()

# Example insert
if __name__ == "__main__":
    insert_report(1, "Severe anemia detected.", "Severe anemia, at high risk.", "Anemia", "High Risk")
    print("Report Inserted")
