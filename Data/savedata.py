import psycopg2
import os
import uuid
import urllib.parse as urlparse

def connect_to_postgres(db_name, table_name):
    try:
        db_url = os.environ.get("DATABASE_URL")
        if db_url is None:
            raise ValueError("DATABASE_URL not set in environment variables!")

        urlparse.uses_netloc.append("postgres")
        parsed_url = urlparse.urlparse(db_url)

        connection = psycopg2.connect(
            database=db_name,
            user=parsed_url.username,
            password=parsed_url.password,
            host=parsed_url.hostname,
            port=parsed_url.port
        )

        cursor = connection.cursor()

        # Create table if not exists
        if table_name == "users":
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    user_id UUID UNIQUE NOT NULL,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL,
                    email TEXT NOT NULL,
                    dob DATE,
                    gender TEXT,
                    user_type TEXT
                );
            """)
        elif table_name == "menu":
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS menu (
                    id SERIAL PRIMARY KEY,
                    food_name TEXT NOT NULL,
                    description TEXT,
                    price NUMERIC(10, 2),
                    food_pic TEXT
                );
            """)
        else:
            raise ValueError(f"Unsupported table: {table_name}")

        connection.commit()
        return connection, cursor

    except ValueError as err:
        print(f"Error: {err}")
        return None, None
    except psycopg2.OperationalError as err:
        print(f"Operational error: {err}")
        return None, None
    except psycopg2.Error as err:
        print(f"Database error: {err}")
        return None, None
