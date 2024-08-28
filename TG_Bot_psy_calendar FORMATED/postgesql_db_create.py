import psycopg2


db_params = {
    'host': '127.0.0.1',
    'port': '5432',
    'user': 'username', #db user
    'password': 'pass', #db pass
    'database': 'name'  # db name
}

# connecting to db
conn = psycopg2.connect(**db_params)
cursor = conn.cursor()

# check if db exists'user_auth'
cursor.execute("SELECT 1 FROM pg_database WHERE datname='user_auth'")
exists = cursor.fetchone()

if not exists:
    # create  db if not exist
    cursor.execute('CREATE DATABASE user_auth')

# close db
conn.close()

db_params['database'] = 'dbname'  #db name
conn = psycopg2.connect(**db_params)
cursor = conn.cursor()

# create table for users
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id SERIAL PRIMARY KEY,
        status TEXT
    )
''')

# save changes in db
conn.commit()

# show user info from table
cursor.execute("SELECT * FROM users")
users = cursor.fetchall()
for user in users:
    user_id, status = user
    print(f"User ID: {user_id}, Status: {status}")

# close connection
cursor.close()
conn.close()
