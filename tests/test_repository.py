from datetime import date, datetime
import sqlite3

import pytest

from expenses_bot.db import repository
from expenses_bot.db.models import Category, Expense


@pytest.fixture(autouse=True)
def create_categories(conn: sqlite3.Connection):
    conn.executemany(
        "INSERT INTO category (name) VALUES (?)",
        (
            ("Продукты",),
            ("Бытовая химия",),
            ("Фаст фуд",),
            ("Транспорт",),
            ("Машина",),
            ("Разовые",),
        ),
    )


def test_get_all_categories(conn: sqlite3.Connection):
    categories = repository.get_all_categories(conn)

    assert len(categories) > 0


def test_create_category(conn: sqlite3.Connection):
    repository.create_category(conn, "Новая")
    rows = conn.execute("SELECT * FROM category").fetchall()

    assert rows[-1] == (7, "Новая")


def test_get_category_by_id(conn: sqlite3.Connection):
    cid = 3

    category = repository.get_category_by_id(conn, cid)

    assert category == Category("Фаст фуд")


def test_missing_get_category_by_id(conn: sqlite3.Connection):
    cid = 69

    with pytest.raises(ValueError):
        _ = repository.get_category_by_id(conn, cid)


def test_create_expenses(conn: sqlite3.Connection):
    current_date = datetime.now().date()
    expenses = (
        Expense(
            category="Продукты",
            amount=69.0,
            created_at=current_date,
        ),
        Expense(
            category="Бытовая химия",
            amount=42.69,
            created_at=current_date,
        ),
    )

    repository.create_expenses(conn, expenses)
    data = conn.execute("SELECT * FROM expense").fetchall()

    assert len(data) > 0
    assert data[0] == (1, 1, 69.0, current_date.strftime("%Y-%m-%d"))
    assert data[1] == (2, 2, 42.69, current_date.strftime("%Y-%m-%d"))


def test_get_all_expenses(conn: sqlite3.Connection):
    conn.execute(
        """
    INSERT INTO expense (category_id, amount, created_at)
    VALUES 
    (1, 69.0, "1970-01-01"), 
    (2, 42.69, "1970-01-01")
    """
    )

    expenses = repository.get_all_expenses(conn)

    assert len(expenses) > 0
    assert expenses[0] == Expense(
        category="Продукты",
        amount=69.0,
        created_at=date.fromisoformat("1970-01-01"),
    )
    assert expenses[1] == Expense(
        category="Бытовая химия",
        amount=42.69,
        created_at=date.fromisoformat("1970-01-01"),
    )


def test_get_expense_by_id(conn: sqlite3.Connection):
    conn.execute(
        """
    INSERT INTO expense (category_id, amount, created_at)
    VALUES 
    (1, 69.0, "1970-01-01"), 
    (2, 42.69, "1970-01-01")
    """
    )

    expense = repository.get_expense_by_id(conn, eid=2)

    assert expense == Expense(
        category="Бытовая химия",
        amount=42.69,
        created_at=date.fromisoformat("1970-01-01"),
    )


def test_missing_get_expense_by_id(conn: sqlite3.Connection):
    conn.execute(
        """
    INSERT INTO expense (category_id, amount, created_at)
    VALUES 
    (1, 69.0, "1970-01-01"), 
    (2, 42.69, "1970-01-01")
    """
    )

    with pytest.raises(ValueError):
        _ = repository.get_expense_by_id(conn, eid=69)


def test_get_expenses_starts_with_date(conn: sqlite3.Connection):
    conn.execute(
        """
    INSERT INTO expense (category_id, amount, created_at)
    VALUES 
    (1, 69.0, "1970-01-01"), 
    (2, 42.69, "2025-01-01")
    """
    )

    expenses = repository.get_expenses_starts_with_date(
        conn, date.fromisoformat("2025-01-01")
    )

    assert len(expenses) == 1
    assert expenses[0] == Expense(
        category="Бытовая химия",
        amount=42.69,
        created_at=date.fromisoformat("2025-01-01"),
    )


def test_get_all_users(conn: sqlite3.Connection):
    conn.execute(
        """
    INSERT INTO user (user_id) VALUES (69), (42)
        """
    )

    users = repository.get_all_users(conn)

    assert len(users) == 2


def test_create_user(conn: sqlite3.Connection):
    repository.create_user(conn, 69)
    repository.create_user(conn, 42)

    users = conn.execute("SELECT * FROM user").fetchall()

    assert len(users) == 2
