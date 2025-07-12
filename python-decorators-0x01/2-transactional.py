import sqlite3
import functools
from datetime import datetime

def transactional(func):
    @functools.wraps(func)
    def transactional_wrapper(*args, **kwargs):
        conn = args[0]
        current_time = datetime.now()
        if conn:
            try:
                result = func(*args, **kwargs)
                print(f"{current_time.strftime("%H:%M:%S")}: Commiting transaction!")
                conn.commit()
                return result
            except Exception as e:
                print(f"{current_time.strftime("%H:%M:%S")}: Error occurred, rolling back!")
                conn.rollback()
                raise e
        else:
            return None
    return transactional_wrapper


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
@transactional
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))
#### Update user's email with automatic transaction handling

update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
