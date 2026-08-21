from sqlite3 import Connection
import sqlite3
from .database import TABLE_LECTURE, create_connection
from ..logger import Logger
import re

COURSE_CODE = 'CC'                          # Enrollment.CC CHAR(20)
SUBJECT_CODE = 'S_code'                     # S_code, integer Subjects.Subject_code
TIME = 'Time'                               # CHAR(10) HH:MM
DATE = 'Date'                               # CHAR(12) DD/MM/YYYY
LECTURE_NAME = 'L_name'                     # CHAR(50)
LECTURER_ID = 'Lecturer_id'                 # INTEGER (Lectures.Lecture_id)

class Lecture:
    _conn: Connection = None

    def __init__(self):
        self._conn = create_connection()

    def create_table(self, conn:Connection=None):
        if None != conn:
            self._conn = conn

        cursor = conn.cursor()
        sql = f'''CREATE TABLE IF NOT EXISTS {TABLE_LECTURE} (
                    _ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    {SUBJECT_CODE} INTEGER NOT NULL,
                    {COURSE_CODE} CHAR(20) NOT NULL,
                    {TIME} CHAR(10) NOT NULL,
                    {DATE} CHAR(12) NOT NULL,
                    {LECTURE_NAME} CHAR(50) NOT NULl,
                    {LECTURER_ID} INTEGER NOT NULL
        )'''
        cursor.execute(sql)
        conn.commit()

    def add(self, subject_id:int = -1, c_code:str = None, time:str = None, date:str = None, l_name:str = None, l_id:int = -1):
        if subject_id < 0:
            raise ValueError('Subject ID should be provided!')

        if l_id < 0:
            raise ValueError('Invalid lecturer id!!')

        if l_name == None or len(l_name) > 50:
            raise ValueError('Invalid lecture name.')

        if c_code == None or len(c_code) > 20:
            raise ValueError('Invalid course code.')

        if time == None or not re.match(r"^(?:[01]\d|2[0-3]):[0-5]\d$", time):
            raise ValueError('Invalid time (fmt. HH:MM)')
        
        if date == None or not re.match(r"^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/\d{4}$", date):
            raise ValueError('Invalid date (fmt. DD/MM/YYYY)')

        if self._conn == None:
            raise ValueError('No connection established.')

        cursor = self._conn.cursor()
        sql = f'''
            INSERT INTO {TABLE_LECTURE} ({SUBJECT_CODE}, {COURSE_CODE}, {TIME}, {DATE}, {LECTURE_NAME}, {LECTURER_ID}) VALUES (?, ?, ?, ?, ?, ?)
        '''

        try:
            cursor.execute(sql, (subject_id, c_code, time, date, l_name, l_id))
            self._conn.commit()
            Logger().d('Insert successfully!!')
        except sqlite3.IntegrityError:
            Logger().e("Integrity Error!!")

    def search_by_subject(self, subject_code:int = -1):
        if self._conn == None:
            raise ValueError('No connection established.')

        cursor = self._conn.cursor()
        if subject_code >= 0:
            cursor.execute(f'SELECT * from {TABLE_LECTURE} where {SUBJECT_CODE} = ?', (subject_code,))
        rows = cursor.fetchall()
        return rows

    def search_by_course(self, c_code:str = None):
        if self._conn == None:
            raise ValueError('No connection established.')

        cursor = self._conn.cursor()
        if c_code != None:
            cursor.execute(f'SELECT * from {TABLE_LECTURE} where {COURSE_CODE} = ?', (c_code,))
        rows = cursor.fetchall()
        return rows