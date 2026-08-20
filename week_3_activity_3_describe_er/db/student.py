from sqlite3 import Connection

FIRST_NAME = 'F_name'
LAST_NAME = 'L_name'
NID = 'NID'
BIRTHDATE = 'B_date'

TABLE_NAME = 'Student'

class Student:
    def __init__(self, conn:Connection=None):
        if None == conn:
            raise ValueError('A sqlite3 connection is needed.')

        cursor = conn.cursor()
        sql = f'CREATE TABLE IF NOT EXISTS {TABLE_NAME} (' \
            f'{FIRST_NAME} TEXT NOT NULL,' \
            f'{LAST_NAME} TEXT NOT NULL,' \
            f'{NID} CHAR(16) PRIMARY KEY,' \
            f'{BIRTHDATE} DATE'
        ')'
        cursor.execute(sql)
        conn.commit()