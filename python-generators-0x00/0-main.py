import seed


def main():
    connection = seed.connect_db()
    if connection:
        print(connection.is_connected())
        seed.create_database(connection)
        connection = seed.connect_to_prodev()
        if connection:
            # seed.create_table(connection)
            # seed.insert_data(connection, "user_data.csv")
            cursor = connection.cursor()
            cursor.execute(f"SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = 'ALX_prodev';")
            result = cursor.fetchone()
            if result:
                print(f"Database ALX_prodev is present ")
            cursor.execute(f"SELECT * FROM user_data LIMIT 5;")
            rows = cursor.fetchall()
            print(rows)
            cursor.close()


main()
