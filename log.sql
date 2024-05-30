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
CREATE TABLE friendships (
    user1id INTEGER NOT NULL,
    user2id INTEGER NOT NULL,
    FOREIGN KEY(member1id) REFERENCES users(id),
    FOREIGN KEY(member2id) REFERENCES users(id)
);

CREATE TABLE scores (
    u1id INTEGER NOT NULL,
    u2id INTEGER,
    verified INTEGER,
);

