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
  
@with_db_connection
def get_user_by_id(conn, user_id):
  cursor = conn.cursor()
  cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
  return cursor.fetchone()

user = get_user_by_id(user_id=1) # type: ignore
print(user)