from datetime import datetime, timedelta
import sqlite3

import pytest

from expenses_bot.core import expense
from expenses_bot.db.models import Expense


def test_cant_parse_input():
    with pytest.raises(ValueError):
        _ = expense.parse_expenses_from_input("69")


def test_correct_parse_one_expense():
    user_input = "69 продукты"
    current_date = datetime.now().date()
    expect = (Expense("продукты", 69, current_date),)

    response = expense.parse_expenses_from_input(user_input)

    assert response == expect


def test_correct_parse_two_expenses():
    user_input = "69 продукты\nбытовая химия 42.69"
    current_date = datetime.now().date()
    expect = (
        Expense("продукты", 69, current_date),
        Expense("бытовая химия", 42.69, current_date),
    )

    response = expense.parse_expenses_from_input(user_input)

    assert response == expect


def test_today_expenses(conn: sqlite3.Connection):
    conn.executemany(
        "INSERT INTO category (name) VALUES (?)",
        (
            ("Продукты",),
            ("Бытовая химия",),
        ),
    )
    conn.execute(
        """
    INSERT INTO expense (category_id, amount, created_at)
    VALUES 
    (1, 69.0, "1970-01-01"), 
    (2, 42.69, "{current_date}")
    """.format(
            current_date=datetime.now().date().isoformat()
        )
    )
    expect = (Expense("Бытовая химия", 42.69, datetime.now().date()),)

    response = expense.get_expenses_by_period(conn, "today")

    assert response == expect


def test_week_expenses(conn: sqlite3.Connection):
    conn.executemany(
        "INSERT INTO category (name) VALUES (?)",
        (
            ("Продукты",),
            ("Бытовая химия",),
        ),
    )
    conn.execute(
        """
    INSERT INTO expense (category_id, amount, created_at)
    VALUES 
    (1, 69.0, "1970-01-01"), 
    (2, 42.69, "{current_date}"),
    (2, 42.69, "{last_week}")
    """.format(
            current_date=datetime.now().date().isoformat(),
            last_week=(datetime.now() - timedelta(days=7)).date().isoformat(),
        )
    )
    expect = (
        Expense("Бытовая химия", 42.69, datetime.now().date()),
        Expense(
            "Бытовая химия",
            42.69,
            (datetime.now() - timedelta(days=7)).date(),
        ),
    )

    response = expense.get_expenses_by_period(conn, "week")

    assert response == expect


def test_current_month_expenses(conn: sqlite3.Connection):
    conn.executemany(
        "INSERT INTO category (name) VALUES (?)",
        (
            ("Продукты",),
            ("Бытовая химия",),
        ),
    )
    conn.execute(
        """
    INSERT INTO expense (category_id, amount, created_at)
    VALUES 
    (1, 69.0, "1970-01-01"), 
    (2, 42.69, "{current_date}"),
    (2, 42.69, "{current_month}")
    """.format(
            current_date=datetime.now().date().isoformat(),
            current_month=datetime.now().replace(day=1).date().isoformat(),
        )
    )
    expect = (
        Expense("Бытовая химия", 42.69, datetime.now().date()),
        Expense(
            "Бытовая химия",
            42.69,
            datetime.now().replace(day=1).date(),
        ),
    )

    response = expense.get_expenses_by_period(conn, "month")

    assert response == expect
