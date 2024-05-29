CREATE TABLE users (
    id INTEGER PRIMARY KEY UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    hash TEXT NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL
);
CREATE TABLE habits (
    user_id INTEGER NOT NULL,
    habit TEXT NOT NULL,
    start_time NUMERIC NOT NULL,
    enter_time NUMERIC NOT NULL,
    streak INTEGER,
    FOREIGN KEY(user_id) REFERENCES users(id)
);

