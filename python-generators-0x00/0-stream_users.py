import seed


def stream_users():
    """Generator function that yields user data from a list of users in the db"""
    connection = seed.connect_to_prodev()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM user_data;")
        for row in cursor:
            yield row
        cursor.close()
    else:
        raise Exception("Failed to connect to the database.")
