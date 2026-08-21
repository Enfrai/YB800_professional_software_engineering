from sqlite3 import Connection
import sqlite3
from database import TABLE_STUDENT, create_connection
import re
from lib.logger import Logger

FIRST_NAME = 'F_name'   # CHAR(30)
LAST_NAME = 'L_name'    # CHAR(30)
NID = 'NID'             # Integer autoincrement
BIRTHDATE = 'B_date'    # CHAR(10)
EMAIL = 'S_email'       # TEXT

class Student:
    _conn: Connection = None

    def __init__(self):
        pass

    def create_table(self, conn:Connection=None):
        if None == conn:
            raise ValueError('A sqlite3 connection is needed.')

        self._conn = conn

        cursor = conn.cursor()
        sql = f'CREATE TABLE IF NOT EXISTS {TABLE_STUDENT} (' \
            f'{NID} INTEGER PRIMARY KEY AUTOINCREMENT,' \
            f'{FIRST_NAME} CHAR(30) NOT NULL,' \
            f'{LAST_NAME} CHAR(30) NOT NULL,' \
            f'{BIRTHDATE} CHAR(10)', \
            f'{EMAIL} TEXT NOT NULL UNIQUE' \
        ')'
        cursor.execute(sql)
        conn.commit()

    def add(self, first_name:str, last_name:str, b_date:str, email:str):
        if first_name == None or len(first_name) > 30:
            raise ValueError('First name cannot be none or longer than 30.')

        if last_name == None or len(last_name) > 30:
            raise ValueError('Last name cannot be none or longer than 30.')

        if b_date != None and not re.match(r"^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/\d{4}$"):
             raise ValueError('Invalid birthdate, please input again by DD/MM/YYYY.')

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