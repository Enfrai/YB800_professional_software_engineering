from sqlite3 import Connection
import sqlite3
from .database import TABLE_SUBJECTS, create_connection
from ..logger import Logger

SUBJECT_CODE = 'Subject_code'               # INTEGER PRIMARY KEY
SUBJECT_UNIT = 'Subject_unit'               # TEXT NOT NULL
SUBJECT_DESC = 'Subject_desc'               # TEXT NOT NULL

class Subjects:
    _conn: Connection = None

    def __init__(self):
        self._conn = create_connection()

    def create_table(self, conn:Connection=None):
        if None != conn:
            self._conn = conn

        cursor = conn.cursor()
        sql = f'''CREATE TABLE IF NOT EXISTS {TABLE_SUBJECTS} (
                    {SUBJECT_CODE} INTEGER PRIMARY KEY AUTOINCREMENT,
                    {SUBJECT_UNIT} TEXT NOT NULL,
                    {SUBJECT_DESC} TEXT NOT NULL
        )'''
        cursor.execute(sql)
        conn.commit()

    def add(self, s_unit:str = None, s_desc:str = None):
        if s_unit == None:
            raise ValueError('Invalid subject unit.')

        if s_desc == None:
            raise ValueError('Invalid subject description.')

        if self._conn == None:
            raise ValueError('No connection established.')

        cursor = self._conn.cursor()
        sql = f'''
            INSERT INTO {TABLE_SUBJECTS} ({SUBJECT_UNIT}, {SUBJECT_DESC}) VALUES (?, ?)
        '''

        try:
            cursor.execute(sql, (s_unit, s_desc))
            self._conn.commit()
            Logger().d('Insert successfully!!')
        except sqlite3.IntegrityError:
            Logger().e("Integrity Error!!")

    def all_subjects(self):
        if self._conn == None:
            raise ValueError('No connection established.')

        cursor = self._conn.cursor()
        cursor.execute(f'SELECT * from {TABLE_SUBJECTS}')
        rows = cursor.fetchall()
        return rows

    def search(self, subject_code:int = -1):
        if self._conn == None:
            raise ValueError('No connection established.')

        cursor = self._conn.cursor()
        if subject_code >= 0:
            cursor.execute(f'SELECT * from {TABLE_SUBJECTS} where {SUBJECT_CODE} = ?', (subject_code,))
        rows = cursor.fetchall()
        return rows
