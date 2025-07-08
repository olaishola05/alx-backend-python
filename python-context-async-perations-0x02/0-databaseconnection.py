import mysql.connector
from mysql.connector import Error

class DatabaseConnection:
    def __init__(self, db_name, user, password, host='localhost', port=3306):
        self.db_name = db_name
        self.user = user
        self.password = password
        self.host = host
        self.port = port

    def __enter__(self):
        print(f"Connecting to the MySQL database {self.db_name}...")
        try:
            self.conn = mysql.connector.connect(
                database=self.db_name,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            print(f"Connection to {self.db_name} successful.")
            return self.conn.cursor()
        except Error as e:
            print(f"Error connecting to database: {e}")
            raise

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn and self.conn.is_connected():
            self.conn.commit()
            self.conn.close()
            print(f"Connection to {self.db_name} closed.")


with DatabaseConnection('user_db', 'root', 'password') as cursor:
    cursor.execute("SELECT * FROM users WHERE user_id = %s", (1,))
    user = cursor.fetchone()
    print(user)