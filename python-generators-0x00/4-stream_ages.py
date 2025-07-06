import seed

def stream_user_ages():
    """Generator function that yields user ages from the database."""
    connection = seed.connect_to_prodev()
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT age FROM user_data;")
        for row in cursor:
            yield row['age']
        cursor.close()
        connection.close()
    else:
        raise Exception("Failed to connect to the database.")
      

def stream_ages():
    """Generator function that yields user ages in a stream."""
    for age in stream_user_ages():
        yield age
    return
  
  
def average_age():
    """Calculate the average age of users."""
    total_age = 0
    count = 0
    for age in stream_ages():
        total_age += age
        count += 1
    if count == 0:
        return 0
    print(f"Average age of users: {total_age / count}")
    return total_age / count