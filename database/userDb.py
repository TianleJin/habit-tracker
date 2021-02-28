import sqlite3

path = 'app.db'
table = 'user'

def get_user_by_id(user_id):
    with sqlite3.connect(path) as conn:
        curs = conn.cursor()
        curs.execute(f'SELECT * from {table} where user_id = ?', (user_id, ))
        return curs.fetchone()

def get_user_by_username(username):
    with sqlite3.connect(path) as conn:
        curs = conn.cursor()
        curs.execute(f'SELECT * from {table} where username = ?', (username, ))
        return curs.fetchone()

def insert_user_into_db(username, password_hash):
    try:
        with sqlite3.connect(path) as conn:
            curs = conn.cursor()
            curs.execute(f'INSERT INTO {table} (username, password) VALUES (?, ?);', (username, password_hash))
            conn.commit()
        return True
    except:
        conn.rollback()
        return False