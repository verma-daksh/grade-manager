import pymysql as sqlcon
def connect():
    return sqlcon.connect(
        host="localhost",
        user="root",
        password="14032007@daksh",
        database="project1"
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