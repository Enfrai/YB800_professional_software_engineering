from sqlite3 import Connection
import sqlite3
from .database import TABLE_ENROLLMENT, TABLE_STUDENT, create_connection
from ..logger import Logger
from .student import FIRST_NAME, LAST_NAME, NID

STUDENT_CODE = 'Student_code'               # Student.NID
DATE_OF_ENROLLMENT = 'Date_of_enrolment'    # TEXT
COURSE_NAME = 'Course_name'                 # CHAR(50)
COURSE_CODE = 'CC'                          # CHAR(20)

class Enrollment:
    _conn: Connection = None

    def __init__(self):
        self._conn = create_connection()

    def create_table(self, conn:Connection=None):
        if None != conn:
            self._conn = conn

        cursor = conn.cursor()
        sql = f'''CREATE TABLE IF NOT EXISTS {TABLE_ENROLLMENT} (
                    _ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    {STUDENT_CODE} INTEGER NOT NULL,
                    {DATE_OF_ENROLLMENT} TEXT DEFAULT (datetime(\'now\', \'localtime\')),
                    {COURSE_NAME} CHAR(50) NOT NULL,
                    {COURSE_CODE} CHAR(20) NOT NULL
        )'''
        cursor.execute(sql)
        conn.commit()

    def add(self, s_id:int = -1, c_name:str = None, c_code:str = None):
        if s_id < 0:
            raise ValueError('Student ID should be provided!')

        if c_name == None or len(c_name) > 50:
            raise ValueError('Invalid course name.')

        if c_code == None or len(c_code) > 20:
             raise ValueError('Invalid course code.')

        if self._conn == None:
            raise ValueError('No connection established.')

        cursor = self._conn.cursor()

        cursor.execute(f'SELECT * FROM {TABLE_ENROLLMENT} WHERE {STUDENT_CODE} = ? AND {COURSE_CODE} = ?', (s_id, c_code))
        rows = cursor.fetchall()
        if len(rows) > 0:
            Logger().d('Already existed!!')
            return

        sql = f'''
            INSERT INTO {TABLE_ENROLLMENT} ({STUDENT_CODE}, {COURSE_NAME}, {COURSE_CODE}) VALUES (?, ?, ?)
        '''

        try:
            cursor.execute(sql, (s_id, c_name, c_code))
            self._conn.commit()
            Logger().d('Insert successfully!!')
        except sqlite3.IntegrityError:
            Logger().e("Integrity Error!!")

    def delete(self, s_id: int = -1):
        if s_id < 0:
            raise ValueError('NID or email has to be provided.')

        if self._conn == None:
            raise ValueError('No connection established.')

        cursor = self._conn.cursor()
        cursor.execute(f'DELETE from {TABLE_ENROLLMENT} where {STUDENT_CODE} = ?', (s_id,))
        self._conn.commit()

    def search(self, s_id:int = -1):
        if s_id < 0:
            return None
        
        if self._conn == None:
            raise ValueError('No connection established.')

        cursor = self._conn.cursor()
        cursor.execute(f'SELECT * from {TABLE_ENROLLMENT} where {STUDENT_CODE} = ?', (s_id,))
        rows = cursor.fetchall()
        return rows

    def count_students_for_each_course(self):
        cursor = self._conn.cursor()
        cursor.execute(f'''
            SELECT {COURSE_NAME}, {COURSE_CODE}, COUNT({STUDENT_CODE}) FROM {TABLE_ENROLLMENT} GROUP BY {COURSE_CODE}
        ''')
        rows = cursor.fetchall()
        return rows

    def list_students_for_more_than_one_course(self):
        cursor = self._conn.cursor()
        cursor.execute(f'''
            SELECT E.{STUDENT_CODE}, S.{FIRST_NAME}, S.{LAST_NAME} 
            FROM {TABLE_ENROLLMENT} AS E
            INNER JOIN {TABLE_STUDENT} AS S
            ON E.{STUDENT_CODE} = S.{NID}
            GROUP BY E.{STUDENT_CODE} 
            HAVING COUNT(DISTINCT E.{COURSE_CODE}) > 1
        ''')
        rows = cursor.fetchall()
        return rows