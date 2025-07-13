import sqlite3
from datetime import datetime

class ExecuteQuery(object):
    def __init__(self, query, params=()):
        self.current_time = datetime.now()
        self.conn = None
        self.query = query
        self.params = params

    def __enter__(self):
        try:
            print(f"{self.current_time.strftime("%H:%M:%S")}: Connecting to the database.")
            self.conn = sqlite3.connect('users.db')
            self.cursor = self.conn.cursor()
            self.cursor.execute(self.query, self.params)
            result = self.cursor.fetchall()
            print(f"{self.current_time.strftime("%H:%M:%S")}: Connected Succesfully!.")
            print(f"{self.current_time.strftime("%H:%M:%S")}: Results: {result}")
            return result
        except Exception as e:
            print(f"Error occured while connecting to the database: {e}")
            raise e

    def __exit__(self, type, value, traceback):
        self.conn.close()
        print(f"{self.current_time.strftime("%H:%M:%S")}: Connection Closed Succesfully!.")

with ExecuteQuery("SELECT * FROM users WHERE age > ?", (25,)) as results:
    print(results)
