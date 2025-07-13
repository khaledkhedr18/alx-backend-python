import time
import sqlite3
import functools
from datetime import datetime

query_cache = {}

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


def cache_query(func):
    @functools.wraps(func)
    def cache_wrapper(*args, **kwargs):
        query = kwargs['query']
        if query in query_cache:
            return query
        else:
            result = func(*args, **kwargs)
            query_cache[query] = result
            return result
    return cache_wrapper


@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

#### First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")

#### Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")
