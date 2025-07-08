import functools
import sqlite3
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

query_cache = {}

def cache_query(func):
  @functools.wraps(func)
  def wrapper(*args, **kwargs):
    query = kwargs.get('query')
    if query is None and args:
      query = args[0]
    try:
      key = (func.__name__, query)
      now = time.time()
      if key in query_cache:
        result, timestamp = query_cache[key]
        if now - timestamp < 60:
          print(f"Cache hit for query: {query}")
          return result
      else:
        print(f"Cache miss for query: {query}")
        result = func(*args, **kwargs)
        query_cache[key] = (result, now)
        return result
    except Exception as e:
      print(f"Error occurred while caching query: {e}")
      raise
  return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()
  
  
users = fetch_users_with_cache(query="SELECT * FROM users") # type: ignore
print(users)

users_again = fetch_users_with_cache(query="SELECT * FROM users") # type: ignore
print(users_again)
