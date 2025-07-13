import sqlite3
from datetime import datetime

class DatabaseConnection(object):

    def __init__(self):
        self.conn = None
        self.current_time = datetime.now()

    def __enter__(self):
        try:
            print(f"{self.current_time.strftime("%H:%M:%S")}: Connecting to the database.")
            self.conn = sqlite3.connect('users.db')
            print(f"{self.current_time.strftime("%H:%M:%S")}: Connected Succesfully!.")
            return self.conn
        except Exception as e:
            print(f"Error occured while connecting to the database: {e}")
            raise e

    def __exit__(self, type, value, traceback):
        self.conn.close()
        print(f"{self.current_time.strftime("%H:%M:%S")}: Connection Closed Succesfully!.")

with DatabaseConnection() as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    print(cursor.fetchall())
