from sqlite3 import Connection
import sqlite3
from database import TABLE_ENROLLMENT, create_connection
import re
from lib.logger import Logger

STUDENT_CODE = 'Student_code'               # Student.NID
DATE_OF_ENROLLMENT = 'Date_of_enrolment'    # TEXT
COURSE_NAME = 'Course_name'                 # CHAR(50)
COURSE_CODE = 'CC'                          # CHAR(20)

class Enrollment:
    _conn: Connection = None

    def __init__(self):
        pass

    def create_table(self, conn:Connection=None):
        if None == conn:
            raise ValueError('A sqlite3 connection is needed.')

        self._conn = conn

        cursor = conn.cursor()
        sql = f'CREATE TABLE IF NOT EXISTS {TABLE_ENROLLMENT} (' \
            f'_ID INTEGER PRIMARY KEY AUTOINCREMENT,' \
            f'{STUDENT_CODE} INTEGER NOT NULL,' \
            f'{DATE_OF_ENROLLMENT} TEXT DEFAULT (datetime(\'now\', \'localtime\')),' \
            f'{COURSE_NAME} CHAR(50) NOT NULl', \
            f'{COURSE_CODE} CHAR(20) NOT NULL' \
        ')'
        cursor.execute(sql)
        conn.commit()

    def add(self, s_id:int = -1, c_name:str = None, c_code:str = None):
        if s_id < 0:
            raise ValueError('Student ID should be provided!')

        if c_name == None or len(c_name) > 50:
            raise ValueError('Invalid course name.')

        if c_code != None or len(c_code) > 20:
             raise ValueError('Invalid course code.')

        if email == None or not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"):
            raise ValueError('Invalid email address, please input again.')

        # all values checked ok, insert them into table.

        if self._conn == None:
            raise ValueError('No connection established.')

        cursor = self._conn.cursor()
        sql = f'''
            INSERT INTO {TABLE_STUDENT} ({FIRST_NAME}, {LAST_NAME}, {BIRTHDATE}, {EMAIL}) VALUES (?, ?, ?, ?)
        '''

        try:
            cursor.execute(sql, (first_name, last_name, b_date, email))
            self._conn.commit()
            Logger().d('Insert successfully!!')
        except sqlite3.IntegrityError:
            Logger().e("Email must be unique!!")

    def delete(self, id: int = -1):
        if id < 0:
            raise ValueError('NID or email has to be provided.')

        if self._conn == None:
            raise ValueError('No connection established.')

        cursor = self._conn.cursor()
        cursor.execute(f'DELETE from {TABLE_STUDENT} where id = ?', (id))
        self._conn.commit()

    def all_users(self):
        if self._conn == None:
            raise ValueError('No connection established.')

        cursor = self._conn.cursor()
        cursor.execute(f'SELECT * from {TABLE_STUDENT}')
        rows = cursor.fetchall()
        return rows

    def search(self, id:int = -1):
        if id < 0:
            return None
        
        if self._conn == None:
            raise ValueError('No connection established.')

        cursor = self._conn.cursor()
        cursor.execute(f'SELECT * from {TABLE_STUDENT} where id = ?', (id))
        rows = cursor.fetchall()