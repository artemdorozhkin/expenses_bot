import sqlite3

from expenses_bot.core.handlers import category
from expenses_bot.infrastructure import repository


def test_missing_category(conn: sqlite3.Connection):
    response = category.handle(conn)

    assert response == "Категории еще не добавлены"


def test_exists_category(conn: sqlite3.Connection):
    repository.create_category(conn, "Продукты")

    response = category.handle(conn)

    assert response == "*ДОБАВЛЕННЫЕ КАТЕГОРИИ*:\nПродукты"


def test_add_category(conn: sqlite3.Connection):
    response = category.handle(conn, "Продукты")

    assert response == "Добавлена категория: Продукты"
