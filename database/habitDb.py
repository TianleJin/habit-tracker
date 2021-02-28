import sqlite3

path = 'app.db'
table = 'habit'

def get_all_habits_for_user(user_id):
    with sqlite3.connect(path) as conn:
        curs = conn.cursor()
        curs.execute(f'SELECT * FROM {table} WHERE user_id = ?', (user_id, ))
        habits = curs.fetchall()
        return list() if habits is None else list(habits)

def insert_habit_for_user(user_id, habit_name, habit_desc):
    try:
        with sqlite3.connect(path) as conn:
            curs = conn.cursor()
            curs.execute(f'INSERT INTO {table} (name, description, user_id) VALUES (?, ?, ?);', (habit_name, habit_desc, user_id))
            conn.commit()
        return True
    except:
        conn.rollback()
        return False

def delete_habit_for_user(user_id, habit_id):
    try:
        with sqlite3.connect(path) as conn:
            curs = conn.cursor()
            curs.execute(f'DELETE FROM {table} WHERE user_id = ? AND habit_id = ?', (user_id, habit_id))
            conn.commit()
        return True
    except:
        conn.rollback()
        return False