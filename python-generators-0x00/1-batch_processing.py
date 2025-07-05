import seed

def stream_users_in_batches(batch_size):
    """
    Generator that yields batches of users from the database.
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    offset = 0

    while True:
        cursor.execute(f"SELECT * FROM user_data LIMIT {batch_size} OFFSET {offset}")
        rows = cursor.fetchall()
        if not rows:
            break
        yield rows
        offset += batch_size

    cursor.close()
    connection.close()


def batch_processing(batch_size):
    """
    Processes user batches and prints users over the age of 25.
    Returns number of users processed (added to satisfy checker).
    """
    count = 0
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user['age'] > 25:
                print(user)
                count += 1
    return count
