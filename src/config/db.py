import os
import psycopg2

DB_HOST = os.environ.get("DB_HOST", "localhost")  # Default to 'localhost' if not set
DB_NAME = os.environ.get("DB_NAME", "booking_db")
DB_USER = os.environ.get("DB_USER", "postgres")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "admin")

# PostgreSQL Database Connection
def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

def test_db_connection():
    try:
        conn = get_db_connection()  # Attempt to connect
        print("Connection successful!")
        
        # Execute a simple query
        with conn.cursor() as cursor:
            cursor.execute("SELECT version();")  # Query to get PostgreSQL version
            db_version = cursor.fetchone()
            print("Database Version:", db_version)
        
        conn.close()  # Always close the connection
        print("Connection closed successfully.")
    except OperationalError as e: # type: ignore
        print("Error while connecting to the database:", e)
    except Exception as ex:
        print("An unexpected error occurred:", ex)