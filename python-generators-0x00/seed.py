import os
import mysql.connector
from mysql.connector import errorcode
from dotenv import load_dotenv
import csv
import uuid as UUID

load_dotenv("../.env")


def validate_env():
    required_keys = ['DB_HOST', 'DB_USER', 'DB_PASSWORD']
    missing_keys = [key for key in required_keys if key not in os.environ]

    if missing_keys:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_keys)}")
    else:
        print("All required environment variables are set.")
        return True


def connect_db():
    connection = None
    try:
        if validate_env():
            print("Connecting to the database server...")
            connection = mysql.connector.connect(
                host=os.getenv('DB_HOST'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD'),
            )
            print("Connection established successfully.")
            print(f"Connected: {connection.is_connected()}")
        return connection
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print(f"Something is wrong with your user name or password: {err}")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    except Exception as e:
        print(f"An error occurred: {e}")


def create_database(connection):
    cursor = connection.cursor()
    try:
        print("Creating database ALX_prodev...")
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        print("Database created successfully.")
    except mysql.connector.Error as err:
        print(f"Failed creating database: {err}")


def connect_to_prodev():
    connection = connect_db()
    if connection:
        try:
            print("Connecting to ALX_prodev database...")
            connection.database = 'ALX_prodev'
            print("Connected to ALX_prodev database.")
            return connection
        except mysql.connector.Error as err:
            print(f"Failed to connect to database: {err}")
    else:
        print("Failed to connect to the database server.")


def create_table(connection):
    cursor = connection.cursor()
    try:
        print("Creating user_data table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
          user_id CHAR(36) PRIMARY KEY,
          name VARCHAR(100) NOT NULL,
          email VARCHAR(100) NOT NULL UNIQUE,
          age DECIMAL(3, 0) NOT NULL
            )
        """)
        print("Table created successfully.")
    except mysql.connector.Error as err:
        print(f"Failed creating table: {err}")


def insert_data(connection, data_file):
    cursor = connection.cursor()
    try:
        count = 0
        for user in csv_user_generator(data_file):
            user['user_id'] = UUID.uuid4().hex
            query = "INSERT IGNORE INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s)"
            value = (user['user_id'], user['name'], user['email'], user['age'])
            cursor.execute(query, value)
            count += 1
        connection.commit()
        print(f"{count} records processed successfully.")
    except mysql.connector.Error as err:
        print(f"Failed inserting data: {err}")
        connection.rollback()


def csv_user_generator(csv_file):
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield row
