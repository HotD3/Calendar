from database import check_database_connection
from token_and_credentials import bot
import psycopg2
from get_db_params import get_db_params



def authorized_only(func):
    def wrapper(message, *args, **kwargs):
        user_id = message.from_user.id
        user_status = check_user_status(user_id)

        if user_status == 'approved':
            return func(message, *args, **kwargs)
        else:
            bot.send_message(user_id, "Для використовування цієї функції потрібно авторизуватись.")
    return wrapper


def update_user_status(user_id, new_status):
    try:
        conn = psycopg2.connect(**get_db_params())
        cursor = conn.cursor()

        cursor.execute("UPDATE users SET status = %s WHERE user_id = %s", (new_status, user_id))
        conn.commit()
        conn.close()

        print(f"Статус пользователя {user_id} обновлен на {new_status}")
        return True
    except Exception as e:
        print(f"Error updating user status: {e}")
        return False

def check_user_exists(user_id):
    try:
        conn = psycopg2.connect(**get_db_params())
        cursor = conn.cursor()

        cursor.execute('SELECT user_id FROM users WHERE user_id = %s', (user_id,))
        row = cursor.fetchone()

        conn.close()

        return row is not None
    except psycopg2.Error as e:
        print(f"Error executing SQL query: {e}")
        return False

def check_user_status(user_id):
    if not check_database_connection():
        print("No connection to the database.")
        return None

    try:
        conn = psycopg2.connect(**get_db_params())
        cursor = conn.cursor()

        cursor.execute('SELECT status FROM users WHERE user_id = %s', (user_id,))
        row = cursor.fetchone()

        if row is not None:
            status = row[0]
            conn.close()
            print(f"Статус пользователя {user_id}: {status}")
            return status
        else:
            conn.close()
            print(f"Пользователь с user_id {user_id} отсутствует в базе данных.")
            return None
    except psycopg2.Error as e:
        print(f"Error executing SQL query: {e}")
        return None
    
def insert_user(user_id, status):
    try:
        conn = psycopg2.connect(**get_db_params())
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (user_id, status) VALUES (%s, %s)', (user_id, status))
        conn.commit()
    except Exception as e:
        print(f"Error inserting user into the database: {e}")
    finally:
        if conn:
            conn.close()


