import seed

def stream_users_in_batches(batch_size):
    """Stream user data in batches using a single database connection."""
    connection = seed.connect_to_prodev()
    if not connection:
        raise Exception("Failed to connect to the database.")
    
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data;")
        
        while True:
            batch = cursor.fetchmany(batch_size)
            if not batch:
                break
            yield batch
    finally:
        cursor.close()
        connection.close()
    return

def batch_processing(batch_size):
    """Process user data in batches."""
    for batch in stream_users_in_batches(batch_size):
        print(f"Processing batch of size {len(batch)}")
        for user in batch:
          if int(user['age']) > 25:
            print(user)
        print("Batch processed successfully.")
    return