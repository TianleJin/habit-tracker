import sqlite3

path = 'app.db'
habit_table = 'habit'
record_table = 'record'

def get_all_records_for_user(user_id, date_string):
    with sqlite3.connect(path) as conn:
        curs = conn.cursor()
        curs.execute(f'''
            SELECT
                r.record_date, h.name, h.habit_id, r.status 
            FROM 
                {habit_table} h JOIN {record_table} r 
                ON h.habit_id = r.habit_id 
            WHERE 
                h.user_id = ?
                AND r.record_date = ?
            ;
        ''', (user_id, date_string))
        records = curs.fetchall()
        return list() if records is None else list(records)

def get_completed_habits_count_for_user(user_id):
    with sqlite3.connect(path) as conn:
        curs = conn.cursor()
        curs.execute(f'''
            SELECT
                r.record_date, count(*)
            FROM 
                {habit_table} h JOIN {record_table} r 
                ON h.habit_id = r.habit_id
            WHERE 
                h.user_id = ?
            GROUP BY
                r.record_date
            HAVING
                r.status = 1
            ;
        ''', (user_id, ))
        records = curs.fetchall()
        return dict(records)

def check_record_exists(habit_id, date_string):
    with sqlite3.connect(path) as conn:
        curs = conn.cursor()
        curs.execute(f'SELECT * FROM {record_table} WHERE habit_id = ? AND record_date = ?', (habit_id, date_string))
        if curs.fetchone() is None:
            return False
        return True

def insert_record_for_habit(habit_id, date_string):
    with sqlite3.connect(path) as conn:
        conn.execute("PRAGMA foreign_keys = 1;")
        try:
            curs = conn.cursor()
            curs.execute(f'INSERT INTO {record_table} (record_date, habit_id) VALUES (?, ?)', (date_string, habit_id))
            conn.commit()
            return True
        except:
            conn.rollback()
            return False

def update_record_for_habit(habit_id, date_string, status):
    with sqlite3.connect(path) as conn:
        conn.execute("PRAGMA foreign_keys = 1;")
        try:
            curs = conn.cursor()
            curs.execute(f'UPDATE {record_table} SET status = ? WHERE record_date = ? AND habit_id = ?', (status, date_string, habit_id))
            conn.commit()
            return True
        except:
            conn.rollback()
            return False