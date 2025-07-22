import sqlite3

import pytest

from expenses_bot.core import user
from expenses_bot.db import repository


def test_correct_add_user(conn: sqlite3.Connection):
    response = user.execute(conn, "/user add 69")

    assert response == "Пользователь 69 добавлен"


def test_correct_rm_user(conn: sqlite3.Connection):
    response = user.execute(conn, "/user rm 69")

    assert response == "Пользователь 69 удален"


def test_correct_ls_user(conn: sqlite3.Connection):
    repository.create_user(conn, 69)

    response = user.execute(conn, "/user ls")

    assert response == "Список id:\n`69`"


def test_print_usage(conn: sqlite3.Connection):
    with pytest.raises(ValueError) as e:
        _ = user.execute(conn, "/user")

        assert str(e) == f"Недостаточно аргументов\n\n{user.USAGE}"


def test_error_print_usage(conn: sqlite3.Connection):
    with pytest.raises(ValueError) as e:
        _ = user.execute(conn, "/user dd 69")

        assert str(e) == f"Неизвестная команда dd\n\n{user.USAGE}"
