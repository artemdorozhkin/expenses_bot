import sqlite3

from expenses_bot.core import category
from expenses_bot.db import repository


def test_missing_category(conn: sqlite3.Connection):
    response = category.list(conn)

    assert response == "Категории еще не добавлены"


def test_exists_category(conn: sqlite3.Connection):
    repository.create_category(conn, "Продукты")

    response = category.list(conn)

    assert response == "*ДОБАВЛЕННЫЕ КАТЕГОРИИ*\n\nПродукты"


def test_add_category(conn: sqlite3.Connection):
    response = category.add(conn, "Продукты")

    assert response == "Добавлена категория: Продукты"
