def stream_user_data(connection):
    """
    Generator that yields user_data rows one by one.
    """
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM user_data;")
    row = cursor.fetchone()
    while row:
        yield row
        row = cursor.fetchone()
    cursor.close()
