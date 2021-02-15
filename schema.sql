PRAGMA foreign_keys = ON;

CREATE TABLE user(
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password Text NOT NULL
);

CREATE TABLE habit(
	habit_id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT NOT NULL,
	description TEXT,
	user_id INTEGER NOT NULL,
	FOREIGN KEY(user_id) REFERENCES user(user_id) ON DELETE CASCADE
);