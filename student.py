import json
import os
import re

DB_FILE = "students.json"

def load_data():
    if not os.path.exists(DB_FILE):
        return []
    try:
        with open(DB_FILE, "r") as file:
            return json.load(file)
    except json.JSONDecodeError:
        print("Error: Database file is corrupted. Starting with an empty record list.")
        return []

def save_data(students):
    with open(DB_FILE, "w") as file:
        json.dump(students, file, indent=4)

def validate_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email) is not None

def add_student():
    students = load_data()
    print("\n--- Add New Student ---")
    
    roll_no = input("Enter Unique Roll Number/ID: ").strip()
    if any(s['roll_no'] == roll_no for s in students):
        print("Error: A student with this Roll Number already exists!")
        return

    name = input("Enter Student Name: ").strip()
    
    email = input("Enter Email Address: ").strip()
    if not validate_email(email):
        print("Error: Invalid email format!")
        return

    try:
        gpa = float(input("Enter GPA (0.0 - 10.0): "))
        if not (0.0 <= gpa <= 10.0):
            raise ValueError
    except ValueError:
        print("Error: GPA must be a valid number between 0.0 and 10.0.")
        return

    students.append({
        "roll_no": roll_no,
        "name": name,
        "email": email,
        "gpa": gpa
    })
    
    save_data(students)
    print("Success: Student record added successfully!")

def view_students():
    students = load_data()
    if not students:
        print("\nNo student records found.")
        return
    
    print("\n--- Student Records ---")
    for s in students:
        print(f"ID: {s['roll_no']} | Name: {s['name']} | Email: {s['email']} | GPA: {s['gpa']}")

def search_student():
    students = load_data()
    query = input("\nEnter search term (ID or Name): ").strip().lower()
    
    results = [s for s in students if query in s['roll_no'].lower() or query in s['name'].lower()]
    
    if not results:
        print("No matching student records found.")
        return
    
    print(f"\n--- Search Results ({len(results)} found) ---")
    for s in results:
        print(f"ID: {s['roll_no']} | Name: {s['name']} | Email: {s['email']} | GPA: {s['gpa']}")

def update_student():
    students = load_data()
    roll_no = input("\nEnter Roll Number of student to update: ").strip()
    
    for s in students:
        if s['roll_no'] == roll_no:
            print(f"Current details: Name: {s['name']}, Email: {s['email']}, GPA: {s['gpa']}")
            
            new_name = input("Enter new name (leave blank to keep current): ").strip()
            if new_name:
                s['name'] = new_name
                
            new_email = input("Enter new email (leave blank to keep current): ").strip()
            if new_email:
                if validate_email(new_email):
                    s['email'] = new_email
                else:
                    print("Error: Invalid email format. Email update skipped.")
                    
            new_gpa = input("Enter new GPA (leave blank to keep current): ").strip()
            if new_gpa:
                try:
                    gpa_val = float(new_gpa)
                    if 0.0 <= gpa_val <= 10.0:
                        s['gpa'] = gpa_val
                    else:
                        print("Error: GPA out of range. GPA update skipped.")
                except ValueError:
                    print("Error: Invalid GPA value. GPA update skipped.")
            
            save_data(students)
            print("Success: Student record updated successfully!")
            return
            
    print("Error: Student with this Roll Number was not found.")

def delete_student():
    students = load_data()
    roll_no = input("\nEnter Roll Number of student to delete: ").strip()
    
    new_students = [s for s in students if s['roll_no'] != roll_no]
    
    if len(new_students) == len(students):
        print("Error: Student record not found.")
        return
        
    save_data(new_students)
    print("Success: Student record deleted successfully!")

def main():
    while True:
        print("\n=== Student Record Management System ===")
        print("1. Add Student")
        print("2. View All Students")
        print("3. Search Student")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Exit")
        
        choice = input("Select an option (1-6): ").strip()
        if choice == '1':
            add_student()
        elif choice == '2':
            view_students()
        elif choice == '3':
            search_student()
        elif choice == '4':
            update_student()
        elif choice == '5':
            delete_student()
        elif choice == '6':
            print("Exiting application. Good luck with your CodeNova internship submission!")
            break
        else:
            print("Invalid choice. Please select between 1 and 6.")

if __name__ == "__main__":
    main()