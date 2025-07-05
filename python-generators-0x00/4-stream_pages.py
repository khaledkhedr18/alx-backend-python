import seed

def stream_user_ages():
    """
    Generator that yields user ages one at a time from the database.
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor()
    cursor.execute("SELECT age FROM user_data")

    for (age,) in cursor:
        yield age

    cursor.close()
    connection.close()


def compute_average_age():
    """
    Computes the average age using the age generator.
    """
    total_age = 0
    count = 0

    for age in stream_user_ages():
        total_age += age
        count += 1

    if count == 0:
        print("No users found.")
    else:
        average = total_age / count
        print(f"Average age of users: {average:.2f}")


if __name__ == "__main__":
    compute_average_age()
