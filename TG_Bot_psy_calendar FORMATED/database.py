import psycopg2
from token_and_credentials import bot
from get_db_params import get_db_params

def check_database_connection():
    try:
        conn = psycopg2.connect(**get_db_params())
        return True
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return False
    finally:
        if conn:
            conn.close()

