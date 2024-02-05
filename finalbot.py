import re
import datetime
from prettytable import PrettyTable
import sqlite3

# Establish connection to the SQLite database
conn = sqlite3.connect('finaldb.db')  # Replace 'your_database_name.db' with your actual database name
cursor = conn.cursor()

# Function to inquire lecture details
def inquire_lecture_details():
    print("The subjects include:")
    
    # Fetch subject details from the database
    cursor.execute("SELECT SubjectCode, SubjectName FROM Subjects;")
    subjects_data = cursor.fetchall()

    # Display subjects in a table using PrettyTable
    subjects_table = PrettyTable()
    subjects_table.field_names = ["Subject Code", "Subject Name"]
    subjects_table.add_rows(subjects_data)
    print(subjects_table)

    while True:
        subject_code_input = input("Please enter the subject code you want to inquire about or press 'exit' to quit: ").strip()

        if subject_code_input.lower() == 'exit':
            print("Exiting the program.")
            break

        # Fetch subject summary from the database
        cursor.execute("SELECT SubjectSummary FROM Subjects WHERE SubjectCode = ?;", (subject_code_input,))
        subject_summary = cursor.fetchone()

        if subject_summary:
            print("Subject Summary:", subject_summary[0])
        else:
            print("Invalid subject code. Please enter a valid subject code.")

        # Fetch chapters for the selected subject from the database
        cursor.execute("SELECT ChapterID, ChapterNumber, ChapterTitle FROM Chapters WHERE SubjectID = (SELECT SubjectID FROM Subjects WHERE SubjectCode = ?);", (subject_code_input,))
        chapters_data = cursor.fetchall()

        # Display chapters in a table using PrettyTable
        chapters_table = PrettyTable()
        chapters_table.field_names = ["Chapter ID", "Chapter Number", "Chapter Title"]
        chapters_table.add_rows(chapters_data)
        print(chapters_table)

        while True:
            chapter_id_input = input("Please enter the Chapter ID you want to inquire about or press 'exit' to quit: ").strip()

            if chapter_id_input.lower() == 'exit':
                print("Exiting the program.")
                break

            # Fetch chapter content from the database
            cursor.execute("SELECT ChapterContent FROM Chapters WHERE ChapterID = ?;", (chapter_id_input,))
            chapter_content = cursor.fetchone()

            if chapter_content:
                print("Chapter Content:", chapter_content[0])
                break
            else:
                print("Invalid Chapter ID. Please enter a valid Chapter ID.")

# Dummy timetable data for testing
timetable_data = [
    {'day_of_week': 'Monday', 'start_time': '09:00:00', 'end_time': '10:00:00', 'subject': 'CST-502'},
    {'day_of_week': 'Monday', 'start_time': '10:00:00', 'end_time': '11:00:00', 'subject': 'CS-504( AA )'},
    {'day_of_week': 'Monday', 'start_time': '11:00:00', 'end_time': '12:00:00', 'subject': 'CS-504 ( NLP )'},
    {'day_of_week': 'Monday', 'start_time': '12:30:00', 'end_time': '13:30:00', 'subject': 'CS-503'},
    {'day_of_week': 'Monday', 'start_time': '13:30:00', 'end_time': '14:30:00', 'subject': 'CS-502'},
    {'day_of_week': 'Monday', 'start_time': '14:30:00', 'end_time': '15:30:00', 'subject': 'CS-505( ERP )'},
    {'day_of_week': 'Tuesday', 'start_time': '09:00:00', 'end_time': '10:00:00', 'subject': 'CST-501'},
    {'day_of_week': 'Tuesday', 'start_time': '10:00:00', 'end_time': '11:00:00', 'subject': 'English'},
    {'day_of_week': 'Tuesday', 'start_time': '11:00:00', 'end_time': '12:00:00', 'subject': 'English'},
    {'day_of_week': 'Tuesday', 'start_time': '12:30:00', 'end_time': '13:30:00', 'subject': 'Self-Study'},
    {'day_of_week': 'Tuesday', 'start_time': '13:30:00', 'end_time': '14:30:00', 'subject': 'CS-503( Lab )'},
    {'day_of_week': 'Tuesday', 'start_time': '14:30:00', 'end_time': '15:30:00', 'subject': 'CS-503( Lab )'},
    {'day_of_week': 'Wednesday', 'start_time': '09:00:00', 'end_time': '10:00:00', 'subject': 'CS-505'},
    {'day_of_week': 'Wednesday', 'start_time': '10:00:00', 'end_time': '11:00:00', 'subject': 'English'},
    {'day_of_week': 'Wednesday', 'start_time': '11:00:00', 'end_time': '12:00:00', 'subject': 'CST-501'},
    {'day_of_week': 'Wednesday', 'start_time': '12:30:00', 'end_time': '13:30:00', 'subject': 'Self-Study'},
    {'day_of_week': 'Wednesday', 'start_time': '13:30:00', 'end_time': '14:30:00', 'subject': 'Self-Study'},
    {'day_of_week': 'Wednesday', 'start_time': '14:30:00', 'end_time': '15:30:00', 'subject': 'Self-Study'},
    {'day_of_week': 'Thursday', 'start_time': '09:00:00', 'end_time': '10:00:00', 'subject': 'CS-505 ( DM/ERP )'},
    {'day_of_week': 'Thursday', 'start_time': '10:00:00', 'end_time': '11:00:00', 'subject': 'CS-504 ( AI )'},
    {'day_of_week': 'Thursday', 'start_time': '11:00:00', 'end_time': '12:00:00', 'subject': 'CST-501'},
    {'day_of_week': 'Thursday', 'start_time': '12:30:00', 'end_time': '13:30:00', 'subject': 'CS-504 ( AA )'},
    {'day_of_week': 'Thursday', 'start_time': '13:30:00', 'end_time': '14:30:00', 'subject': 'Self-Study'},
    {'day_of_week': 'Thursday', 'start_time': '14:30:00', 'end_time': '15:30:00', 'subject': 'Self-Study'},
    {'day_of_week': 'Friday', 'start_time': '09:00:00', 'end_time': '10:00:00', 'subject': 'CST-502( Lab )'},
    {'day_of_week': 'Friday', 'start_time': '10:00:00', 'end_time': '11:00:00', 'subject': 'CS-504( Lab )'},
    {'day_of_week': 'Friday', 'start_time': '11:00:00', 'end_time': '12:00:00', 'subject': 'CS-505( Lab )'},
    {'day_of_week': 'Friday', 'start_time': '12:30:00', 'end_time': '13:30:00', 'subject': 'CS-505( WE )'},
    {'day_of_week': 'Friday', 'start_time': '13:30:00', 'end_time': '14:30:00', 'subject': 'Self-Study'},
    # Add more data for other days and subjects
]

# Function to get the timetable for a specific day
def get_timetable(day: str) -> str:
    timetable_for_day = [entry for entry in timetable_data if entry['day_of_week'].lower() == day.lower()]

    if timetable_for_day:
        table = PrettyTable()
        table.field_names = ["Start Time", "End Time", "Subject"]
        for entry in timetable_for_day:
            table.add_row([entry['start_time'], entry['end_time'], entry['subject']])
        message = f"Timetable for {day}:\n{table}"
    else:
        message = f"No timetable available for {day}."

    return message

# Function to get the full timetable
def get_full_timetable() -> str:
    table = PrettyTable()
    table.field_names = ["Day", "Start Time", "End Time", "Subject"]
    for entry in timetable_data:
        table.add_row([entry['day_of_week'], entry['start_time'], entry['end_time'], entry['subject']])
    message = f"Full Timetable:\n{table}"

    return message

# Function to get the timetable for today
def get_timetable_for_today() -> str:
    current_day = datetime.datetime.now().strftime('%A')
    return get_timetable(current_day)

# Main function for timetable checking
def check_timetables():
    print("If you want to check the timetable, type 'timetable for today' or any day you want to inquire about.")
    print("To exit the conversation, type 'exit'.")

    while True:
        user_input = input("You: ").lower()

        if user_input == 'exit' or re.search(r'\b(bye|goodbye)\b', user_input):
            print("Goodbye! Have a great day.")
            break

        # Check for timetable-related commands using regular expressions
        if re.search(r'\b(timetable for \w+|timetable for today|timetable for tomorrow|timetable)\b', user_input):
            if 'for' in user_input:
                day = user_input.split('for')[-1].strip()
                if day.lower() == 'today':
                    # User requested timetable for today
                    print("Bot:", get_timetable_for_today())
                elif day.lower() == 'tomorrow':
                    # Calculate the timetable for tomorrow
                    tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
                    day = tomorrow.strftime('%A')
                    print("Bot:", get_timetable(day))
                else:
                    # User requested timetable for a specific day
                    print("Bot:", get_timetable(day))
            else:
                # User requested the full timetable
                print("Bot:", get_full_timetable())
        else:
            print("Bot: I'm sorry, I didn't understand that. Please use one of the specified commands.")


# Main function
def main():
    print("Welcome to the UCSY Final Year Bot!")
    print("Choose an option:")
    print("1. Check Timetables")
    print("2. Inquire lecture details")

    option = input("Enter your choice (1 or 2): ")

    if option == '1':
        check_timetables()

    elif option == '2':
        inquire_lecture_details()

    else:
        print("Invalid option. Please choose 1 or 2.")


if __name__ == "__main__":
    main()

# Close the database connection when done
conn.close()