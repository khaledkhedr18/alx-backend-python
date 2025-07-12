import sqlite3
import functools
from datetime import datetime

def with_db_connection(func):
    @functools.wraps(func)
    def db_connection_wrapper(*args, **kwargs):
        current_time = datetime.now()
        try:
            print(f"{current_time.strftime("%H:%M:%S")}: Connecting to the database.")
            conn = sqlite3.connect('users.db')
            print(f"{current_time.strftime("%H:%M:%S")}: Connected Succesfully!.")
            result = func(conn, *args, **kwargs)
            print(f"Results: {result}")
            return result
        except sqlite3.Error as e:
            print(f"Error connecting to the database: {e}")
        finally:
            print(f"{current_time.strftime("%H:%M:%S")}: Closing Connection!")
            conn.close()
    return db_connection_wrapper

@with_db_connection
def get_user_by_id(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()
#### Fetch user by ID with automatic connection handling

user = get_user_by_id(user_id=1)
print(user)
