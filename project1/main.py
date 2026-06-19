from database import (
    create_table, add_student, get_allstudents,
    update_marks, delete_student, get_average
)
def assign_grade(marks):
    if marks >= 90:
        return "A+"
    elif marks >= 75:
        return "A"
    elif marks >= 60:
        return "B"
    elif marks >= 45:
        return "C"
    else:
        return "F"
def display_students(students):
    if not students:
        print("No students found")
        return
    print("{:<5} {:<20} {:<15} {:<10} {:<5}".format( "ID", "Name", "Subject", "Marks", "Grade"))
    print("-" * 60)
    for row in students:
        student_id, name, subject, marks = row
        grade = assign_grade(marks)
        print("{:<5} {:<20} {:<15} {:<10} {:<5}".format(student_id, name, subject, marks, grade))
def main():
    create_table()
    while True :
        print("\n===== Student Grade Manager =====")
        print("1. Add student")
        print("2. View all students (leaderboard)")
        print("3. Update marks")
        print("4. Delete student")
        print("5. View class average")
        print("6. Exit")
        choice = int(input("enter your choice ="))
        if choice == 1:
            name = input("student name :")
            subject = input("subject :")
            try:
                marks = float(input("marks(0-100):"))
                if not 0<marks<100:
                    print("marks should be between 0-100")
                    continue
                add_student(name, subject, marks)
                print(f"Added,{name},succesfully!")
            except ValueError:
                print("Invalid value ")
        elif choice == 2:
            students= get_allstudents()
            display_students(students)
        elif choice == 3:
            try:
                student_id = int(input("enter your new id:"))
                new_marks = float(input("enter your new_marks:"))
                update_marks(student_id, new_marks)
                print("marks updated!")
            except ValueError:
                print("Invalid value")
        elif choice == 4:
            try:
                student_id=int(input("enter your studentid :"))
                delete_student(student_id)
            except ValueError:
                print("Invalid value")
        elif choice == 5:
            avg = get_average()
            print("the class average is :", avg)
        elif choice == 6:
            print("goodbye")
            break
        else:
            print("invalid choice.try again")
if __name__ == "__main__":
    main()
            