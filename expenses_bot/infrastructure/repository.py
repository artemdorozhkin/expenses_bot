from datetime import date
import sqlite3

from expenses_bot.core.models import Category, Expense


def create_user(conn: sqlite3.Connection, user_id: int):
    conn.execute("INSERT INTO user (user_id) VALUES (?)", (user_id,))


def remove_user(conn: sqlite3.Connection, user_id: int):
    conn.execute("DELETE FROM user WHERE user_id = ?", (user_id,))


def get_all_users(conn: sqlite3.Connection) -> list[int]:
    rows = conn.execute("SELECT user_id FROM user").fetchall()
    return [user_id for (user_id,) in rows]


def get_all_categories(conn: sqlite3.Connection, user_id: int) -> list[Category]:
    categories = conn.execute(
        "SELECT * FROM category AND user_id = ?", (user_id,)
    ).fetchall()
    return [Category(name) for _, name in categories]


def get_category_by_id(conn: sqlite3.Connection, cid: int, user_id: int) -> Category:
    row = conn.execute(
        "SELECT * FROM category WHERE id = ? AND user_id = ?", (cid, user_id)
    ).fetchone()
    if not row:
        raise ValueError(f"incorrect category id '{cid}'")

    return Category(name=row[1])


def create_category(conn: sqlite3.Connection, name: str, user_id: int):
    conn.execute("INSERT INTO category (name, user_id) VALUES (?, ?)", (name, user_id))


def get_expenses_starts_with_date(
    conn: sqlite3.Connection,
    start_date: date,
    user_id: int,
) -> list[Expense]:
    rows = conn.execute(
        "SELECT * FROM expense WHERE created_at >= ? AND user_id = ?",
        (start_date, user_id),
    )

    expenses = []
    for _, category_id, amount, created_at in rows:
        category = get_category_by_id(conn, category_id, user_id)

        expenses.append(
            Expense(
                category=category.name,
                amount=amount,
                created_at=date.fromisoformat(created_at),
            )
        )
    return expenses


def get_all_expenses(conn: sqlite3.Connection, user_id: int) -> list[Expense]:
    rows = conn.execute(
        "SELECT * FROM expense WHERE user_id = ?", (user_id,)
    ).fetchall()

    expenses = []
    for _, category_id, amount, created_at in rows:
        category = get_category_by_id(conn, category_id, user_id)

        expenses.append(
            Expense(
                category=category.name,
                amount=amount,
                created_at=date.fromisoformat(created_at),
            )
        )
    return expenses


def get_expense_by_id(conn: sqlite3.Connection, eid: int, user_id: int) -> Expense:
    row = conn.execute(
        "SELECT * FROM expense WHERE id = ? AND user_id = ?", (eid, user_id)
    ).fetchone()

    if not row:
        raise ValueError(f"incorrect expense id '{eid}'")

    _, category_id, amount, created_at = row
    category = get_category_by_id(conn, cid=category_id, user_id=user_id)
    return Expense(
        category=category.name,
        amount=amount,
        created_at=date.fromisoformat(created_at),
    )


def create_expenses(
    conn: sqlite3.Connection,
    expenses: tuple[Expense, ...],
    user_id: int,
):
    cursor = conn.cursor()

    categories = cursor.execute("SELECT * FROM category WHERE user_id = ?", (user_id,))
    category_map = {name: cid for cid, name in categories.fetchall()}

    for e in expenses:
        if e.category not in category_map:
            create_category(conn, e.category, user_id)
            category_map[e.category] = cursor.lastrowid

    insert_data = (
        (category_map[e.category], e.amount, e.created_at, user_id) for e in expenses
    )

    conn.executemany(
        "INSERT INTO expense (category_id, amount, created_at, user_id) VALUES (?, ?, ?, ?)",
        insert_data,
    )
