import sqlite3

import pytest

from expenses_bot.core import validators


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


def test_correct_category(conn: sqlite3.Connection):
    user_input = "продукты"

    is_valid, result = validators.validate_category(conn, user_input)

    assert is_valid == True
    assert "Продукты" == result


def test_guess_category(conn: sqlite3.Connection):
    user_input = "транспортные"

    is_valid, result = validators.validate_category(conn, user_input)

    assert is_valid == False
    assert "Транспорт" == result


def test_not_guess_category(conn: sqlite3.Connection):
    user_input = "Без категории"

    is_valid, result = validators.validate_category(conn, user_input)

    assert is_valid == False
    assert result is None
