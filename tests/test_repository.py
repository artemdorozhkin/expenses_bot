from datetime import datetime
import sqlite3

import pytest

from expenses_bot import repository
from expenses_bot.models import Expense


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
    categories = repository.get_all_categories(conn)

    assert categories[-1].name == "Новая"


def test_create_expenses(conn: sqlite3.Connection):
    current_date = datetime.now().date()
    expenses = [
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
    ]

    repository.create_expenses(conn, expenses)
    data = conn.execute("SELECT * FROM expense").fetchall()

    assert len(data) > 0
    assert data[0] == (1, 1, 69.0, current_date.strftime("%Y-%m-%d"))
    assert data[1] == (2, 2, 42.69, current_date.strftime("%Y-%m-%d"))
