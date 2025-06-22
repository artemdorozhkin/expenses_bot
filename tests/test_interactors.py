from datetime import datetime
import sqlite3

from expenses_bot.core import interactors
from expenses_bot.infrastructure import repository


def test_cant_parse_input(conn: sqlite3.Connection):
    user_input = "69"

    response = interactors.handle_expanse_input(conn, user_input)

    assert response == (
        "Не удалось получить данные о расходах. "
        "Необходимо прислать сообщение в формате:\n"
        "`69 категория`"
    )


def test_cant_find_expense_category(conn: sqlite3.Connection):
    user_input = "69 продукты"

    response = interactors.handle_expanse_input(conn, user_input)

    assert response == "Не удалось найти категорию 'продукты'.\nДобавить?"


def test_guess_category(conn: sqlite3.Connection):
    repository.create_category(conn, "Продукты")
    user_input = "69 продукт"

    response = interactors.handle_expanse_input(conn, user_input)

    current_date = datetime.now().date().strftime("%d.%m.%Y")
    assert response == (
        "Не удалось найти категорию '*продукт*'.\nВозможно имелась ввиду категория '*Продукты*'?"
    )


def test_correct_parse_one_expense(conn: sqlite3.Connection):
    repository.create_category(conn, "Продукты")
    user_input = "69 продукты"

    response = interactors.handle_expanse_input(conn, user_input)

    current_date = datetime.now().date().strftime("%d.%m.%Y")
    assert response == (
        "Категория: Продукты\n" "Сумма: 69.0\n\n" f"Дата: {current_date}"
    )


def test_correct_parse_two_expenses(conn: sqlite3.Connection):
    repository.create_category(conn, "Продукты")
    repository.create_category(conn, "Бытовая химия")
    user_input = "69 продукты\nбытовая химия 42.69"

    response = interactors.handle_expanse_input(conn, user_input)

    current_date = datetime.now().date().strftime("%d.%m.%Y")
    assert response == (
        "Категория: Продукты\n"
        "Сумма: 69.0\n"
        "Категория: Бытовая химия\n"
        "Сумма: 42.69\n\n"
        f"Дата: {current_date}"
    )
