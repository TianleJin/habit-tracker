import sqlite3

path = 'app.db'
table = 'habit'

def table_exist():
    with sqlite3.connect(path) as conn:
        curs = conn.cursor()
        curs.execute('SELECT count(name) FROM sqlite_master WHERE type="table" AND name=?', (table, ))
        return curs.fetchone()[0] == 1

def get_all_habits_for_user(user_id):
    if not table_exist():
        return False

    with sqlite3.connect(path) as conn:
        curs = conn.cursor()
        curs.execute(f'SELECT * FROM {table} WHERE user_id = ?', (user_id, ))
        habits = curs.fetchall()
        return list() if habits is None else list(habits)

def insert_habit_for_user(user_id, habit_name, habit_desc):
    if not table_exist():
        return False

    with sqlite3.connect(path) as conn:
        try:
            curs = conn.cursor()
            curs.execute(f'INSERT INTO {table} (name, description, user_id) VALUES (?, ?, ?);', (habit_name, habit_desc, user_id))
            conn.commit()
            return True
        except:
            conn.rollback()
            return False

def update_habit_for_user(user_id, habit_id, habit_desc):
    if not table_exist():
        return False

    with sqlite3.connect(path) as conn:
        try:
            curs = conn.cursor()
            curs.execute(f'UPDATE {table} SET description = ? WHERE user_id = ? AND habit_id = ?;', (habit_desc, user_id, habit_id))
            conn.commit()
            return True
        except:
            conn.rollback()
            return False

def delete_habit_for_user(user_id, habit_id):
    if not table_exist():
        return False

    with sqlite3.connect(path) as conn:
        try:
            curs = conn.cursor()
            curs.execute(f'DELETE FROM {table} WHERE user_id = ? AND habit_id = ?', (user_id, habit_id))
            conn.commit()
            return True
        except:
            conn.rollback()
            return False