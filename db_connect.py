import mysql.connector as connection
from datetime import datetime
import os

# Database Configuration
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "12345",  # Update with your MySQL password if different
}

DB_NAME = "simple_registration_db"
DB_NAME = "students"
def setup_database():
    # Connect to MySQL ServER
    
    conn = connection.connect(host="localhost",user="root", passwd="12345", use_pure=True  )
    cursor = conn.cursor() # a memory area to run SQL statement 
    
    # Create and use the database
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    cursor.execute(f"USE {DB_NAME}")
    
    # Create Students Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100),
        matrix_number VARCHAR(20) UNIQUE,
        course VARCHAR(100),
        gender VARCHAR(10),
        date_registered DATETIME
    )
    """)
    conn.commit()
    cursor.close()
    conn.close()
    print("Database 'students' table is ready.")

setup_database()
def get_conn():
    # Helper function to get connection directly to our active database
    return connection.connect(**DB_CONFIG, database=DB_NAME)

def insert_student(name, matrix, course, gender):
    conn = get_conn()
    cursor = conn.cursor()
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    query = "INSERT INTO students (name, matrix_number, course, gender, date_registered) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(query, (name, matrix, course, gender, current_time))
    conn.commit()
    conn.close()

def fetch_all_students():
    conn = get_conn()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM students")
    records = cursor.fetchall()
    conn.close()
    return records

def update_student(student_id, name, matrix, course, gender):
    conn = get_conn()
    cursor = conn.cursor()
    query = "UPDATE students SET name=%s, matrix_number=%s, course=%s, gender=%s WHERE id=%s"
    cursor.execute(query, (name, matrix, course, gender, student_id))
    conn.commit()
    conn.close()

def delete_student(student_id):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE id=%s", (student_id,))
    conn.commit()
    conn.close()