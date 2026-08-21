import sqlite3
from sqlite3 import Connection
from ..logger import Logger

DATABASE_NAME = 'college_students.db'

TABLE_STUDENT = 'Student'
TABLE_ENROLLMENT = 'Enrollment'
TABLE_LECTURE = 'Lecture'
TABLE_LECTURER = 'Lecturer'
TABLE_SUBJECTS = 'Subjects'

conn:Connection = None

def create_connection():
    global conn
    if None == conn:
        Logger().d(f'start to connect {DATABASE_NAME} ...')
        conn = sqlite3.connect(DATABASE_NAME)
    return conn

def close_connection():
    global conn
    if None != conn:
        conn.close()

def reset_all():
    global conn
    conn.execute(f'DELETE FROM {TABLE_STUDENT}')
    conn.execute(f'DELETE FROM {TABLE_ENROLLMENT}')
    conn.execute(f'DELETE FROM {TABLE_LECTURE}')
    conn.execute(f'DELETE FROM {TABLE_LECTURER}')
    conn.execute(f'DELETE FROM {TABLE_SUBJECTS}')