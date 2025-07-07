import sqlite3
import functools


def log_queries(func):
  @functools.wraps(func)
  def wrapper(*args, **kwargs):
    query = kwargs.get('query')
    if query is None and args:
      query = args[0]
    print(f"Query passed: {query}")
    try:
      return func(*args, **kwargs)
    except Exception as e:
      print(f"Query failed: {e}")
      raise
  return wrapper


@log_queries
def fetch_all_users(query):
  conn = sqlite3.connect('user_db')
  cursor = conn.cursor()
  cursor.execute(query)
  results = cursor.fetchall()
  conn.close()
  return results

users = fetch_all_users(query="SELECT * FROM users")
print(users)