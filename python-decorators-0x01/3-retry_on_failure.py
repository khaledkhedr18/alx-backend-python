import time
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



def retry_on_failure(retries=3, delay=1):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"Error occurred: {e}")
                    time.sleep(delay)
            raise Exception("Max retries exceeded")
        return wrapper
    return decorator

@with_db_connection
@retry_on_failure(retries=3, delay=1)

def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

#### attempt to fetch users with automatic retry on failure

users = fetch_users_with_retry()
print(users)
