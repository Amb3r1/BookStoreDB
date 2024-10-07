import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Correct the variable name from DB_MAME to DB_NAME
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")


def connect_to_db():
    """
    Connect to the BookStore database and return the connection and cursor.
    """
    try:

        if not all([DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT]):
            raise ValueError("Missing one or more environment variables.")

        connection = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
        )
        cur = connection.cursor()
        return connection, cur

    except psycopg2.Error as e:
        print(f"Error connecting to the database: {e}")
        return None, None


def close_connection(connection, cursor):
    """Close the database connection and cursor."""
    if cursor:
        cursor.close()
    if connection:
        connection.close()
