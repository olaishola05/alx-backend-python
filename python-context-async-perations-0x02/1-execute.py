import sqlite3

class ExecuteQuery:
  def __init__(self, query: str, params: tuple = ()):
    self.query = query
    self.params = params
    
  def __enter__(self):
    print("Connecting to the database...")
    try:
      self.conn = sqlite3.connect('user_db')
      self.cursor = self.conn.cursor()
      print("Connection to the database successful.")
      return self
    except sqlite3.Error as e:
      print(f"Error connecting to the database: {e}")
      raise

  def __exit__(self, exc_type, exc_val, exc_tb):
    if self.conn:
      self.conn.commit()
      self.conn.close()
      print("Connection to the database closed.")
      
  def execute(self):
    try:
      self.cursor.execute(self.query, self.params)
      print("Query executed successfully.")
      return self.cursor
    except sqlite3.Error as e:
      print(f"An error occurred: {e}")
      self.conn.rollback()
      return None
    except Exception as e:
      print(f"An unexpected error occurred: {e}")
      self.conn.rollback()
      return None

# Example usage
query = "SELECT * FROM users WHERE age > ?"
params = (25,)


with ExecuteQuery(query=query, params=params) as query_executor:
    cursor = query_executor.execute()
    if cursor:
        results = cursor.fetchall()
        if results:
            for row in results:
                print(row)
        else:
            print("No results returned.")
    else:
        print("No results returned or an error occurred.")