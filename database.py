import sqlite3

conn = sqlite3.connect(':memory:')

conn.execute("""CREATE TABLE users (
    username TEXT NOT NULL PRIMARY KEY,
    password TEXT NOT NULL
);""")

cur = conn.cursor()

cur.execute("""INSERT INTO users (username, password) VALUES (?, ?);""", ('Jerry', 'Jin'))

conn.commit()

try:
    cur.execute("""INSERT INTO users (username, password) VALUES (?, ?);""", ('Jerry', 'Jin'))
except Exception as e:
    print(e)

cur.execute("""SELECT * FROM users;""")

print(cur.fetchall())

conn.close()z