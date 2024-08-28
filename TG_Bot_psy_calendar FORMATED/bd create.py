import sqlite3
db_path = r'path to user_auth.db'
#connecting to db and create table if not exist
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

#create table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        status TEXT
    )
''')

cursor.execute("SELECT * FROM users")
users = cursor.fetchall()
for user in users:
    user_id, status = user
    print(f"User ID: {user_id},  Status: {status}")

#save and close connection
conn.commit()
conn.close()
