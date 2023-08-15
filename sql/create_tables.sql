DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS user;


CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'user' CHECK(role IN ('admin', 'user'))
);
    
CREATE TABLE transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    amount REAL NOT NULL,
    description TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    transaction_type TEXT NOT NULL DEFAULT 'ausgabe' CHECK(transaction_type IN ('einnahme', 'ausgabe')),
    kontostand FLOAT NOT NULL DEFAULT 0,
    FOREIGN KEY(user_id) REFERENCES user(id)
);

CREATE TABLE budget (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    amount DECIMAL(10,2),
    end_date DATE,
    name TEXT,
    FOREIGN KEY(user_id) REFERENCES user(id)
);

