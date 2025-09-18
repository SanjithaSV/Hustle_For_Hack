from database import create_database
from database_operations import insert_report, update_report, delete_report, search_reports_by_category

# Function to show the menu
def show_menu():
    print("Welcome to the Medical Report Database")
    print("1. Insert a New Report")
    print("2. Update an Existing Report")
    print("3. Delete a Report")
    print("4. Search Reports by Category")
    print("5. Exit")

# Function to get user input for insertion
def get_user_input_and_insert():
    patient_id = int(input("Enter patient ID: "))
    report_text = input("Enter report text: ")
    summary = input("Enter summary: ")
    category = input("Enter report category (e.g., 'Anemia', 'Cardiovascular'): ")
    prediction = input("Enter prediction (e.g., 'High Risk', 'Moderate Risk'): ")

    insert_report(patient_id, report_text, summary, category, prediction)

# Main program to interact with the user
def main():
    create_database()  # Create the database and table if not exists

    while True:
        show_menu()
        choice = input("Choose an option (1-5): ")

        if choice == '1':
            get_user_input_and_insert()  # Insert report
        elif choice == '2':
            report_id = int(input("Enter the report ID to update: "))
            new_report_text = input("Enter new report text: ")
            new_summary = input("Enter new summary: ")
            new_category = input("Enter new category: ")
            new_prediction = input("Enter new prediction: ")
            update_report(report_id, new_report_text, new_summary, new_category, new_prediction)  # Update report
        elif choice == '3':
            report_id = int(input("Enter the report ID to delete: "))
            delete_report(report_id)  # Delete report
        elif choice == '4':
            category = input("Enter the category to search for: ")
            search_reports_by_category(category)  # Search reports by category
        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
