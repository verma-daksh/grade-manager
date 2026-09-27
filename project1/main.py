# =========================================================
# Student Grade Mangement System 
# =========================================================

import pymysql
import sys
from database import (
    connect, create_tables, add_student, get_allstudents,
    search_student, delete_student, get_debarred, add_marks,
    get_marks, calculate_cgpa
)

# ---------------------------------------------------------
# HELPER FUNCTIONS FOR MYSQL OPERATIONS
# ---------------------------------------------------------

def update_student_in_db(s_id, reg, nm, att, rem):
    con = connect()
    cur = con.cursor()
    query = "UPDATE students SET registration_no = %s, name = %s, attendance = %s, remarks = %s WHERE id = %s;"
    cur.execute(query, (reg, nm, float(att), rem, s_id))
    con.commit()
    con.close()


def get_single_student(s_id):
    con = connect()
    cur = con.cursor()
    query = "SELECT * FROM students WHERE id = %s;"
    cur.execute(query, (s_id,))
    row = cur.fetchone()
    con.close()
    return row


def view_all_marks_by_category(table_name):
    students = get_allstudents()
    all_records = []
    
    for st in students:
        s_id = st[0]
        reg = st[1]
        name = st[2]
        marks_list = get_marks(table_name, s_id)
        
        for item in marks_list:
            sub = item[0]
            score = item[1]
            all_records.append((s_id, reg, name, sub, score))
            
    return all_records


# ---------------------------------------------------------
# FORMATTING & DISPLAY FUNCTIONS
# ---------------------------------------------------------

def print_line():
    print("-------------------------------------------------------------------------")


def print_header(title):
    print("\n================================================-------------------------")
    print("   " + title.upper())
    print("================================================-------------------------")


def show_student_records(records):
    if not records:
        print("\n--> No student records found in database!")
        return

    print_line()
    print("%-6s %-16s %-22s %-15s %-12s" % ("ID", "REG NO", "NAME", "ATTENDANCE(%)", "REMARKS"))
    print_line()
    
    for row in records:
        s_id = row[0]
        reg = row[1]
        name = row[2]
        att = row[3]
        rem = row[4] if (len(row) > 4 and row[4]) else "N/A"
        print("%-6d %-16s %-22s %-15.2f %-12s" % (s_id, reg, name, att, rem))
        
    print_line()


def show_marks_records(records, exam_type):
    if not records:
        print(f"\n--> No marks entries found for {exam_type}!")
        return

    print_line()
    print("%-8s %-15s %-20s %-15s %-8s" % ("STD_ID", "REG_NO", "NAME", "SUBJECT", "MARKS"))
    print_line()
    
    for row in records:
        s_id = row[0]
        reg = row[1]
        name = row[2]
        sub = row[3]
        marks = row[4]
        print("%-8d %-15s %-20s %-15s %-8.2f" % (s_id, reg, name, sub, marks))
        
    print_line()


def choose_exam_category():
    print("\n   Select Exam Category:")
    print("   1. CAT-1")
    print("   2. CAT-2")
    print("   3. Term End Exam")
    print("   4. Practical Exam")
    
    cat_ch = input("   Enter Choice (1-4): ").strip()
    
    if cat_ch == "1":
        return "cat1_marks", "CAT-1"
    elif cat_ch == "2":
        return "cat2_marks", "CAT-2"
    elif cat_ch == "3":
        return "termend_marks", "Term End"
    elif cat_ch == "4":
        return "practical_marks", "Practical"
    else:
        return None, None


# ---------------------------------------------------------
# MAIN PROGRAM LOOP
# ---------------------------------------------------------

def main():
    try:
        create_tables()
    except Exception as e:
        print("Database connection error:", e)

    while True:
        print("\n===== VIT Student Grade Manager =====")
        print("1. Add student")
        print("2. Add marks (CAT-1 / CAT-2 / Term End / Practical)")
        print("3. View all students")
        print("4. View marks by exam")
        print("5. Calculate weighted score + CGPA")
        print("6. Check debarred students (attendance < 75%)")
        print("7. Search student by name or registration no.")
        print("8. Update student details")
        print("9. Delete student")
        print("10. Exit")

        ch = input("\nenter your choice = ").strip()

        # Option 1: Add student
        if ch == "1":
            print_header("1. Add New Student Record")
            
            rno = input("Enter Registration Number (e.g. 26BCE1001): ").strip()
            name = input("Enter Student Full Name: ").strip()
            
            if rno == "" or name == "":
                print("\n[!] Registration No and Name cannot be empty!")
                continue

            try:
                att = float(input("Enter Attendance Percentage: "))
                if att < 0 or att > 100:
                    print("\n[!] Attendance percentage should be between 0 and 100!")
                    continue
            except ValueError:
                print("\n[!] Invalid input! Attendance must be a number.")
                continue

            rem = input("Enter Remarks (Optional): ").strip()

            try:
                add_student(rno, name, att, rem)
                print(f"\n[+] Success: Student '{name}' added successfully!")
            except Exception as err:
                print("\n[-] Error adding student:", err)

        # Option 2: Add marks
        elif ch == "2":
            print_header("2. Add Exam Marks")
            
            tbl_name, exam_title = choose_exam_category()
            if not tbl_name:
                print("\n[!] Invalid exam category selected!")
                continue

            try:
                st_id = int(input("\nEnter Student ID: "))
            except ValueError:
                print("\n[!] Invalid Student ID!")
                continue

            st_data = get_single_student(st_id)
            if not st_data:
                print(f"\n[!] Student with ID {st_id} does not exist!")
                continue

            print(f"Selected Student: {st_data[2]} ({st_data[1]})")
            sub_name = input("Enter Subject Name: ").strip()
            
            if sub_name == "":
                print("\n[!] Subject name cannot be empty!")
                continue
           
            if tbl_name in ["cat1_marks", "cat2_marks"]:
                max_mks = 50
            elif tbl_name == "practical_marks":
                max_mks = 40
            else:
                max_mks = 100

            try:
                mks = float(input(f"Enter Marks Scored (0-{max_mks}): "))
                if mks < 0 or mks > max_mks:
                    print("\n[!] Marks should be between 0 and {max_mks}!")
                    continue
            except ValueError:
                print("\n[!] Invalid marks input!")
                continue

            try:
                add_marks(tbl_name, st_id, sub_name, mks)
                print(f"\n[+] Success: {exam_title} marks recorded for {st_data[2]}!")
            except Exception as err:
                print("\n[-] Error inserting marks:", err)

        # Option 3: View all students
        elif ch == "3":
            print_header("3. View All Students")
            data = get_allstudents()
            show_student_records(data)

        # Option 4: View marks by exam
        elif ch == "4":
            print_header("4. View Marks By Exam Category")
            tbl_name, exam_title = choose_exam_category()
            
            if tbl_name:
                marks_data = view_all_marks_by_category(tbl_name)
                show_marks_records(marks_data, exam_title)
            else:
                print("\n[!] Invalid category choice!")

        # Option 5: Calculate weighted score + CGPA
        elif ch == "5":
            print_header("5. Calculate Weighted Score & Grade")
            
            try:
                st_id = int(input("Enter Student ID: "))
            except ValueError:
                print("\n[!] Invalid Student ID!")
                continue

            st_data = get_single_student(st_id)
            if not st_data:
                print(f"\n[!] Student with ID {st_id} not found!")
                continue

            res = calculate_cgpa(st_id)
            if res:
                print("\n" + "=" * 50)
                print(f"   ACADEMIC MARKSHEET: {st_data[2].upper()}")
                print("=" * 50)
                print(f"   Registration No : {st_data[1]}")
                print(f"   Attendance Rate : {st_data[3]}%")
                print("   ----------------------------------------------")
                print(f"   CAT-1 Average (15% weight)   : {res['cat1']}/50")
                print(f"   CAT-2 Average (15% weight)   : {res['cat2']}/50")
                print(f"   Term End Avg  (30% weight)   : {res['termend']}/100")
                print(f"   Practical Avg (40% weight)   : {res['practical']}/40")
                print("   ----------------------------------------------")
                print(f"   WEIGHTED PERCENTAGE          : {res['weighted']}%")
                print(f"   FINAL GRADE                  : {res['grade']}")
                print(f"   GRADE POINTS                 : {res['points']} / 10")
                print("=" * 50)
            else:
                print("\n[!] Incomplete Marks Entry!")
                print("    Student must have marks in ALL 4 categories")
                print("    (CAT-1, CAT-2, Term End, Practical) to compute CGPA.")

        # Option 6: Check debarred students
        elif ch == "6":
            print_header("6. Debarred Students List (Attendance < 75%)")
            debarred_data = get_debarred()
            show_student_records(debarred_data)

        # Option 7: Search student
        elif ch == "7":
            print_header("7. Search Student Database")
            kword = input("Enter Name or Registration No to search: ").strip()
            
            if kword == "":
                print("\n[!] Search keyword cannot be empty!")
                continue

            results = search_student(kword)
            show_student_records(results)

        # Option 8: Update student details
        elif ch == "8":
            print_header("8. Update Student Record")
            
            try:
                st_id = int(input("Enter Student ID to modify: "))
            except ValueError:
                print("\n[!] Invalid Student ID!")
                continue

            st = get_single_student(st_id)
            if not st:
                print(f"\n[!] Student ID {st_id} does not exist!")
                continue

            existing_rem = st[4] if (len(st) > 4 and st[4]) else "None"
            print("\nExisting Details:")
            print(f"- Reg No     : {st[1]}")
            print(f"- Name       : {st[2]}")
            print(f"- Attendance : {st[3]}%")
            print(f"- Remarks    : {existing_rem}\n")

            new_reg = input(f"Enter New Reg No [{st[1]}]: ").strip() or st[1]
            new_name = input(f"Enter New Name [{st[2]}]: ").strip() or st[2]
            
            att_in = input(f"Enter New Attendance % [{st[3]}]: ").strip()
            if att_in == "":
                new_att = st[3]
            else:
                try:
                    new_att = float(att_in)
                except ValueError:
                    print("\n[!] Invalid attendance rate, keeping existing value.")
                    new_att = st[3]

            default_rem = st[4] if (len(st) > 4 and st[4]) else ""
            new_rem = input(f"Enter New Remarks [{default_rem}]: ").strip() or default_rem

            try:
                update_student_in_db(st_id, new_reg, new_name, new_att, new_rem)
                print("\n[+] Success: Student details updated!")
            except Exception as err:
                print("\n[-] Error updating record:", err)

        # Option 9: Delete student
        elif ch == "9":
            print_header("9. Delete Student Record")
            
            try:
                st_id = int(input("Enter Student ID to delete: "))
            except ValueError:
                print("\n[!] Invalid Student ID!")
                continue

            st = get_single_student(st_id)
            if not st:
                print(f"\n[!] Student ID {st_id} does not exist!")
                continue

            ans = input(f"Are you sure you want to delete '{st[2]}'? (y/n): ").strip().lower()
            if ans == "y":
                try:
                    delete_student(st_id)
                    print("\n[+] Success: Student record deleted successfully.")
                except Exception as err:
                    print("\n[-] Error deleting record:", err)
            else:
                print("\n[-] Deletion cancelled.")

        # Option 10: Exit
        elif ch == "10":
            print("\nExiting system... Thank you!")
            sys.exit()

        else:
            print("\n[!] Invalid choice! Please select between 1 and 10.")


if __name__ == "__main__":
    main()