from database import get_db_connection

def get_reports():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM reports")
    reports = cursor.fetchall()
    conn.close()
    return reports

# Retrieve and print all reports
if __name__ == "__main__":
    reports = get_reports()
    for report in reports:
        print(report)
