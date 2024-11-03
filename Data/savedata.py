import psycopg2

def connect_to_postgres(database_name, table_name):
    try:
        connection = psycopg2.connect(
            user='postgres',
            password='Blackcat3394',
            host='127.0.0.1',
            port='5432',
            database=database_name
        )

        cursor = connection.cursor()
        # Example usage: cursor.execute(f"SELECT * FROM {table_name};")

        return connection, cursor

    except psycopg2.OperationalError as err:
        print(f"Operational error: {err}")
        return None, None

    except psycopg2.Error as err:
        print(f"Error: {err}")
        return None, None

if __name__ == '__main__':
    database_name = 'Ruby Treat'
    table_name = 'users'  # Ensure this matches your actual table name
    connection, cursor = connect_to_postgres(database_name, table_name)

    if connection:
        cursor.close()
        connection.close()
