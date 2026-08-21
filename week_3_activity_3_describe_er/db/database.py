import sqlite3
from sqlite3 import Connection
from lib.logger import Logger

DATABASE_NAME = '../output/college_students.db'

TABLE_STUDENT = 'Student'
TABLE_ENROLLMENT = 'Enrollment'
TABLE_LECTURE = 'Lecture'
TABLE_LECTURER = 'Lecturer'
TABLE_SUBJECTS = 'Subjects'

conn:Connection = None

def create_connection():
    if conn == None:
        Logger().d(f'start to connect {DATABASE_NAME} ...')
        conn = sqlite3.connect(DATABASE_NAME)
    return conn

def close_connection():
    if conn != None:
        conn.close()