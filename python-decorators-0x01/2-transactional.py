import sqlite3
import functools

def with_db_connection(func):
  @functools.wraps(func)
  def wrapper(*args, **kwargs):
    with sqlite3.connect('user_db') as conn:
        print("Connecting to the database...")
        if not conn:
            raise Exception("Failed to connect to the database.")
        try:
            print("Connection to db successful!")
            return func(conn, *args, **kwargs)
        except Exception as e:
            print(f"Connection to db failed! {e}")
            raise
  return wrapper

def transactional(func):
    """Decorator to handle transactions for database operations."""
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        cursor = conn.cursor()
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()
            return result
        except Exception as e:
            conn.rollback()
            print(f"Transaction failed: {e}")
            raise
        finally:
            cursor.close()
    return wrapper


@with_db_connection
@transactional
def update_user_name(conn, user_id, new_name):
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET name = ? WHERE user_id = ?", (new_name, user_id))
    result = cursor.rowcount
    if result == 0:
        raise Exception(f"User with ID {user_id} not found.")
    print(f"User {user_id} name updated to {new_name}") 

update = update_user_name(user_id=1, new_name='Jamal') # type: ignore
print(update)