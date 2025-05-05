import psycopg2
import os
import urllib.parse as urlparse

def connect_to_postgres():
    try:
        # Get DATABASE_URL from environment variables
        db_url = os.environ.get("DATABASE_URL")

        if db_url is None:
            raise ValueError("DATABASE_URL not set in environment variables!")

        # Parse the database URL
        urlparse.uses_netloc.append("postgres")
        parsed_url = urlparse.urlparse(db_url)

        # Connect to the database using the parsed URL
        connection = psycopg2.connect(
            database=parsed_url.path[1:],  # database name
            user=parsed_url.username,
            password=parsed_url.password,
            host=parsed_url.hostname,
            port=parsed_url.port
        )

        cursor = connection.cursor()

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
