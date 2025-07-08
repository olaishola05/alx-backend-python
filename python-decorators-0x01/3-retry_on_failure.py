import sqlite3
import functools
import time

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

def retry_on_failure(retries=3, delay=1):
    """Decorator to retry a function call on failure."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"Attempt {attempt + 1} failed: {e}")
                    time.sleep(delay)
            raise Exception(f"All {retries} attempts failed.")
        return wrapper
    return decorator


@with_db_connection
@retry_on_failure(retries=5, delay=2)
def fetch_users_with_retry(conn):
  cursor = conn.cursor()
  cursor.execute("SELECT * FROM users")
  return cursor.fetchall()

users = fetch_users_with_retry() # type: ignore
print(users)