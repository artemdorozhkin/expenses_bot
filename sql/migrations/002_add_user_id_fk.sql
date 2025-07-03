-- add `user_id` as a foreign key for the `category`, `expense` tables

PRAGMA foreign_keys = off;

ALTER TABLE category RENAME TO category_old;

CREATE TABLE IF NOT EXISTS category (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    user_id INTEGER NOT NULL,

    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE
);

INSERT INTO category (id, name, user_id)
SELECT id, name, 1 FROM category_old;

DROP TABLE category_old;

ALTER TABLE expense RENAME TO expense_old;

CREATE TABLE IF NOT EXISTS expense (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_id INTEGER NOT NULL,
    amount REAL NOT NULL,
    created_at DATE NOT NULL,
    user_id INTEGER NOT NULL,

    FOREIGN KEY (category_id) REFERENCES category(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE
);

INSERT INTO expense (id, category_id, amount, created_at, user_id)
SELECT id, category_id, amount, created_at, 1 FROM expense_old;

DROP TABLE expense_old;

PRAGMA foreign_keys = on;