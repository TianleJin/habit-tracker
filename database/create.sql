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

CREATE TABLE record(
	record_date TEXT NOT NULL,
	status INTEGER DEFAULT 0 NOT NULL CHECK(status IN (0, 1)),
	habit_id INTEGER NOT NULL,
	PRIMARY KEY(habit_id, record_date),
	FOREIGN KEY(habit_id) REFERENCES habit(habit_id) ON DELETE CASCADE
);