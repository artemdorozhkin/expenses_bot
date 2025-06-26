import sqlite3

from expenses_bot.core.handlers import user
from expenses_bot.infrastructure import repository


def test_correct_add_user(conn: sqlite3.Connection):
    response = user.handle(conn, "/user add 69")

    assert response == "Пользователь 69 добавлен"


def test_correct_rm_user(conn: sqlite3.Connection):
    response = user.handle(conn, "/user rm 69")

    assert response == "Пользователь 69 удален"


def test_correct_ls_user(conn: sqlite3.Connection):
    repository.create_user(conn, 69)

    response = user.handle(conn, "/user ls")

    assert response == "Список id:\n`69`"


def test_print_usage(conn: sqlite3.Connection):
    response = user.handle(conn, "/user")

    assert response == user.USAGE


def test_error_print_usage(conn: sqlite3.Connection):
    response = user.handle(conn, "/user dd 69")

    assert response == f"Неизвестная команда dd\n\n{user.USAGE}"
