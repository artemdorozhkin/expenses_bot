import sqlite3

from expenses_bot.models import Category, Expense


def get_all_categories(conn: sqlite3.Connection) -> list[Category]:
    categories = conn.execute("SELECT * FROM category").fetchall()
    return [Category(name) for _, name in categories]


def create_category(conn: sqlite3.Connection, name: str):
    conn.execute("INSERT INTO category (name) VALUES (?)", (name,))


def create_expenses(conn: sqlite3.Connection, expenses: list[Expense]):
    cursor = conn.cursor()

    categories = cursor.execute("SELECT * FROM category")
    category_map = {name: cid for cid, name in categories.fetchall()}

    for e in expenses:
        if e.category not in category_map:
            create_category(conn, e.category)
            category_map[e.category] = cursor.lastrowid

    insert_data = ((category_map[e.category], e.amount, e.created_at) for e in expenses)

    conn.executemany(
        "INSERT INTO expense (category_id, amount, created_at) VALUES (?, ?, ?)",
        insert_data,
    )
