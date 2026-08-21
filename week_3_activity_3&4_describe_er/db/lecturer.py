from sqlite3 import Connection
import sqlite3
from .database import TABLE_LECTURER, create_connection
from ..logger import Logger
import re

LECTURER_ID = 'Lecturer_id'                 # INTEGER (Lectures.Lecture_id) PRIMARY KEY
L_LASTNAME = 'L_lastname'                   # CHAR(30)
L_FIRSTNAME = 'L_firstname'                 # CHAR(30)
L_EMAIL = 'L_email'                         # TEXT UNIQUE
L_ADDRESS = 'L_address'                     # TEXT

class Lecturer:
    _conn: Connection = None

    def __init__(self):
        self._conn = create_connection()

    def create_table(self, conn:Connection=None):
        if None != conn:
            self._conn = conn

        cursor = conn.cursor()
        sql = f'''CREATE TABLE IF NOT EXISTS {TABLE_LECTURER} (
                    {LECTURER_ID} INTEGER PRIMARY KEY AUTOINCREMENT,
                    {L_LASTNAME} CHAR(30) NOT NULL,
                    {L_FIRSTNAME} CHAR(30) NOT NULL,
                    {L_EMAIL} TEXT NOT NULL UNIQUE,
                    {L_ADDRESS} TEXT
        )'''
        cursor.execute(sql)
        conn.commit()

    def add(self, first_name:str, last_name:str, address:str, email:str):
        if first_name == None or len(first_name) > 30:
            raise ValueError('First name cannot be none or longer than 30.')

        if last_name == None or len(last_name) > 30:
            raise ValueError('Last name cannot be none or longer than 30.')

        if email == None or not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
            raise ValueError('Invalid email address, please input again.')

        # all values checked ok, insert them into table.

        if self._conn == None:
            raise ValueError('No connection established.')

        cursor = self._conn.cursor()
        sql = f'''
            INSERT INTO {TABLE_LECTURER} ({L_FIRSTNAME}, {L_LASTNAME}, {L_ADDRESS}, {L_EMAIL}) VALUES (?, ?, ?, ?)
        '''

        try:
            cursor.execute(sql, (first_name, last_name, address, email))
            self._conn.commit()
            Logger().d('Insert successfully!!')
        except sqlite3.IntegrityError:
            Logger().e("Email must be unique!!")

    def delete(self, id: int = -1):
        if id < 0:
            raise ValueError('Lecturer id has to be provided.')

        if self._conn == None:
            raise ValueError('No connection established.')

        cursor = self._conn.cursor()
        cursor.execute(f'DELETE from {TABLE_LECTURER} where {LECTURER_ID} = ?', (id,))
        self._conn.commit()

    def all_lecturers(self):
        if self._conn == None:
            raise ValueError('No connection established.')

        cursor = self._conn.cursor()
        cursor.execute(f'SELECT * from {TABLE_LECTURER}')
        rows = cursor.fetchall()
        return rows

    def search(self, id:int = -1):
        if id < 0:
            return None
        
        if self._conn == None:
            raise ValueError('No connection established.')

        cursor = self._conn.cursor()
        cursor.execute(f'SELECT * from {TABLE_LECTURER} where {LECTURER_ID} = ?', (id,))
        rows = cursor.fetchall()
        return rows