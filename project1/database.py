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
    
    

def create_table():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTO_INCREMENT,
            name TEXT NOT NULL,
            subject TEXT NOT NULL,
            marks REAL NOT NULL
        )
    """)
    conn.commit()
    conn.close()
def add_student(name, subject, marks):
    conn=connect()
    cursor=conn.cursor()
    cursor.execute ( 
        "INSERT INTO students (name, subject, marks) VALUES (%s, %s, %s)",
        (name, subject, marks)
    ) 
    conn.commit()
    conn.close()
def get_allstudents():
    conn=connect()
    cursor=conn.cursor()
    cursor.execute( " SELECT * FROM students ORDER BY MARKS DESC;" )
    rows = cursor.fetchall()
    conn.close()
    return rows
def update_marks(student_id, new_marks ):
    conn=connect()
    cursor=conn.cursor()
    cursor.execute(" UPDATE students SET marks= %s WHERE id = %s",
                   (new_marks, student_id,  ))
    conn.commit()
    conn.close()
def delete_student(student_id):
    conn=connect()
    cursor=conn.cursor()
    cursor.execute(
        "DELETE FROM students WHERE id= %s ",(student_id)
    )
    conn.commit()
    conn.close()

def get_average():
    conn=connect()
    cursor=conn.cursor()
    cursor.execute(
        "SELECT AVG(marks) FROM students"
    )
    result=cursor.fetchone()[0]
    conn.close()
    return result if result else 0