import sqlite3


class Database:
    def __init__(self, database_path: str):
        self.conn = sqlite3.connect(database=database_path, check_same_thread=False)
        self.cur = self.conn.cursor()
        self.conn.commit()


    def __del__(self):
        self.conn.close()
