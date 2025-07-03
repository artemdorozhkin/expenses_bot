-- remove `user_id` as a foreign key from the `category`, `expense` tables

PRAGMA foreign_keys = OFF;

ALTER TABLE category RENAME TO category_old;
CREATE TABLE category (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);
INSERT INTO category (id, name)
SELECT id, name FROM category_old;
DROP TABLE category_old;

ALTER TABLE expense RENAME TO expense_old;
CREATE TABLE expense (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_id INTEGER NOT NULL,
    amount REAL NOT NULL,
    created_at DATE NOT NULL,
    FOREIGN KEY (category_id) REFERENCES category(id) ON DELETE CASCADE
);
INSERT INTO expense (id, category_id, amount, created_at)
SELECT id, category_id, amount, created_at FROM expense_old;
DROP TABLE expense_old;

PRAGMA foreign_keys = ON;