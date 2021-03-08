import sqlite3

path = 'app.db'
table = 'user'

def table_exist():
    with sqlite3.connect(path) as conn:
        curs = conn.cursor()
        curs.execute('SELECT count(name) FROM sqlite_master WHERE type="table" AND name=?', (table, ))
        return curs.fetchone()[0] == 1

def get_user_by_id(user_id):
    if not table_exist():
        return False

    with sqlite3.connect(path) as conn:
        curs = conn.cursor()
        curs.execute(f'SELECT * from {table} where user_id = ?', (user_id, ))
        return curs.fetchone()

def get_user_by_username(username):
    if not table_exist():
        return False

    with sqlite3.connect(path) as conn:
        curs = conn.cursor()
        curs.execute(f'SELECT * from {table} where username = ?', (username, ))
        return curs.fetchone()

def insert_user_into_db(username, password_hash):
    if not table_exist():
        return False

    with sqlite3.connect(path) as conn:
        conn.execute("PRAGMA foreign_keys = 1;")
        try:
            curs = conn.cursor()
            curs.execute(f'INSERT INTO {table} (username, password) VALUES (?, ?);', (username, password_hash))
            conn.commit()
            return True
        except:
            conn.rollback()
            return False