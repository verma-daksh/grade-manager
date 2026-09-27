import pymysql as sqlcon
from dotenv import load_dotenv
import os

load_dotenv()

def connect():
    return sqlcon.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )
    
    

def create_tables():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id              INTEGER PRIMARY KEY AUTO_INCREMENT,
            registration_no VARCHAR(20) NOT NULL UNIQUE,
            name            VARCHAR(20) NOT NULL,
            attendance      FLOAT NOT NULL DEFAULT 0,
            remarks         TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cat1_marks (
            id              INTEGER PRIMARY KEY AUTO_INCREMENT,
            student_id      INTEGER NOT NULL,
            subject         VARCHAR(100) NOT NULL, 
            marks           FLOAT NOT NULL,
            FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cat2_marks (
            id              INTEGER PRIMARY KEY AUTO_INCREMENT,
            student_id      INTEGER NOT NULL,
            subject         VARCHAR(100) NOT NULL,
            marks           FLOAT NOT NULL,
            FOREIGN KEY     (student_id) REFERENCES students(id) ON DELETE CASCADE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS termend_marks (
            id              INTEGER PRIMARY KEY AUTO_INCREMENT,
            student_id      INTEGER NOT NULL,
            subject         VARCHAR(100) NOT NULL,
            marks           FLOAT NOT NULL,
            FOREIGN KEY     (student_id) REFERENCES students(id) ON DELETE CASCADE
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS practical_marks (
            id              INTEGER PRIMARY KEY AUTO_INCREMENT,
            student_id      INTEGER NOT NULL,
            subject         VARCHAR(100) NOT NULL,
            marks           FLOAT NOT NULL,
            FOREIGN KEY     (student_id) REFERENCES students(id) ON DELETE CASCADE
        )
    """)
    conn.commit()
    conn.close()

def add_student(registration_no, name, attendance, remarks):
    conn=connect()
    cursor=conn.cursor()
    cursor.execute ( 
        "INSERT INTO students (registration_no, name, attendance, remarks) VALUES (%s, %s, %s, %s)",
        (registration_no, name, attendance, remarks)
    ) 
    conn.commit()
    conn.close()

def get_allstudents():
    conn=connect()
    cursor=conn.cursor()
    cursor.execute( " SELECT * FROM students ORDER BY name;" )
    rows = cursor.fetchall()
    conn.close()
    return rows

def search_student(keyword):
    conn=connect()
    cursor=conn.cursor()
    cursor.execute(" SELECT * FROM students WHERE name LIKE %s OR registration_no LIKE %s",
                   (f"%{keyword}%", f"%{keyword}%" )
    )
    rows = cursor.fetchall()
    conn.close()
    return rows

def delete_student(student_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
    cursor.execute("DELETE FROM students WHERE id = %s;", (student_id,))
    exam_tables = ["cat1_marks", "cat2_marks", "termend_marks", "practical_marks"]
    for tbl in exam_tables:
        cursor.execute(f"DELETE FROM {tbl} WHERE student_id = %s;", (student_id,))
    for tbl in exam_tables:
        cursor.execute(f"UPDATE {tbl} SET student_id = student_id - 1 WHERE student_id > %s;", (student_id,))
    cursor.execute("UPDATE students SET id = id - 1 WHERE id > %s ORDER BY id ASC;", (student_id,))
    cursor.execute("SELECT IFNULL(MAX(id), 0) + 1 FROM students;")
    next_id = cursor.fetchone()[0]
    cursor.execute(f"ALTER TABLE students AUTO_INCREMENT = {int(next_id)};")
    cursor.execute("SET FOREIGN_KEY_CHECKS = 1;") 
    conn.commit()
def get_debarred():
    conn=connect()
    cursor=conn.cursor()
    cursor.execute(
        "SELECT * FROM students WHERE attendance < 75"
    )
    result=cursor.fetchall()
    conn.close()
    return result

def add_marks(table, student_id, subject, marks):
    conn=connect()
    cursor=conn.cursor()
    cursor.execute(
        f"INSERT INTO {table}(student_id, subject, marks) VALUES (%s, %s, %s)",
        (student_id, subject, marks)
    )
    conn.commit()
    conn.close()

def get_marks(table, student_id):
    conn=connect()
    cursor=conn.cursor()
    cursor.execute(
        f"SELECT subject, marks FROM {table} WHERE student_id = %s",
        (student_id,)
    )
    rows = cursor.fetchall()
    conn.close()
    return rows

def assign_grade(weighted):
    if weighted >= 90: return '0', 10
    elif weighted >= 80: return 'A+', 9
    elif weighted >= 70: return 'A', 8
    elif weighted >= 60: return 'B+', 7
    elif weighted >= 50: return 'B', 6
    elif weighted >= 40: return 'C', 5
    else:                return 'F', 0

def calculate_cgpa(student_id):
    cat1 = get_marks("cat1_marks", student_id)
    cat2 = get_marks("cat2_marks", student_id)
    termend = get_marks("termend_marks", student_id)
    practical = get_marks("practical_marks", student_id)
    if not cat1 or not cat2 or not termend or not practical:
        return None
    
    avg_cat1  =  sum(m for _, m in cat1) /len(cat1)
    avg_cat2  =  sum(m for _, m in cat2) /len(cat2)
    avg_termend  =  sum(m for _, m in termend) /len(termend)
    avg_practical  =  sum(m for _, m in practical) /len(practical)

    cat1_pct = (avg_cat1/50.0)*100
    cat2_pct = (avg_cat1/50.0)*100
    practical_pct =(avg_practical/40.0)*100

    weighted =(cat1_pct * 0.15) + (cat2_pct * 0.15) + (avg_termend * 0.30) + (practical_pct * 0.40)
    grade, points = assign_grade(weighted)

    return {
        "cat1":  round(avg_cat1, 2) ,
        "cat2":  round(avg_cat2, 2) ,
        "termend": round(avg_termend, 2),
        "practical": round(avg_practical, 2),
        "weighted": round(weighted, 2) ,
        "grade": grade , 
        "points": points
    }