from datetime import datetime
import sqlite3

from expenses_bot.core import interactors
from expenses_bot.infrastructure import repository


def test_cant_parse_input(conn: sqlite3.Connection):
    user_input = "69"

    response, keyboard = interactors.handle_expanse_input(conn, user_input)

    assert keyboard is None
    assert response == (
        "Не удалось получить данные о расходах\\. "
        "Необходимо прислать сообщение в формате:\n"
        "`69 категория`"
    )


def test_cant_find_expense_category(conn: sqlite3.Connection):
    user_input = "69 продукты"

    response, keyboard = interactors.handle_expanse_input(conn, user_input)

    assert keyboard is not None
    kb_dict = keyboard.to_dict()
    assert "inline_keyboard" in kb_dict
    assert len(kb_dict["inline_keyboard"]) == 1
    buttons = kb_dict["inline_keyboard"][0]
    assert "Добавить: продукты" == buttons[0]["text"]

    assert response == "Не удалось найти категорию *продукты*\\.\nДобавить?"


def test_guess_category(conn: sqlite3.Connection):
    repository.create_category(conn, "Продукты")
    user_input = "69 продукт"

    response, keyboard = interactors.handle_expanse_input(conn, user_input)

    assert keyboard is not None
    kb_dict = keyboard.to_dict()
    assert "inline_keyboard" in kb_dict
    assert len(kb_dict["inline_keyboard"]) == 2
    buttons = kb_dict["inline_keyboard"]
    assert "Добавить: продукт" == buttons[0][0]["text"]
    assert "Выбрать: Продукты" == buttons[1][0]["text"]

    assert response == (
        "Не удалось найти категорию *продукт*\\.\nВозможно имелась ввиду категория *Продукты*?"
    )


def test_correct_parse_one_expense(conn: sqlite3.Connection):
    repository.create_category(conn, "Продукты")
    user_input = "69 продукты"

    response, keyboard = interactors.handle_expanse_input(conn, user_input)

    current_date = datetime.now().date().strftime("%d.%m.%Y")
    assert keyboard is not None
    kb_dict = keyboard.to_dict()
    assert "inline_keyboard" in kb_dict
    assert len(kb_dict["inline_keyboard"]) == 4
    buttons = kb_dict["inline_keyboard"]
    assert "Добавить расход" == buttons[0][0]["text"]
    assert "Изменить категорию" == buttons[1][0]["text"]
    assert "Изменить сумму" == buttons[2][0]["text"]
    assert "Изменить дату" == buttons[3][0]["text"]

    assert response == (
        "Категория: Продукты\n" "Сумма: 69.0\n\n" f"Дата: {current_date}"
    )


def test_correct_parse_two_expenses(conn: sqlite3.Connection):
    repository.create_category(conn, "Продукты")
    repository.create_category(conn, "Бытовая химия")
    user_input = "69 продукты\nбытовая химия 42.69"

    response, keyboard = interactors.handle_expanse_input(conn, user_input)

    current_date = datetime.now().date().strftime("%d.%m.%Y")
    assert keyboard is not None
    kb_dict = keyboard.to_dict()
    assert "inline_keyboard" in kb_dict
    assert len(kb_dict["inline_keyboard"]) == 4
    buttons = kb_dict["inline_keyboard"]
    assert "Добавить расход" == buttons[0][0]["text"]
    assert "Изменить категорию" == buttons[1][0]["text"]
    assert "Изменить сумму" == buttons[2][0]["text"]
    assert "Изменить дату" == buttons[3][0]["text"]

    assert response == (
        "Категория: Продукты\n"
        "Сумма: 69.0\n"
        "Категория: Бытовая химия\n"
        "Сумма: 42.69\n\n"
        f"Дата: {current_date}"
    )


def test_correct_add_user(conn: sqlite3.Connection):
    response = interactors.handle_user(conn, "/user add 69")

    assert response == "Пользователь 69 добавлен"


def test_correct_rm_user(conn: sqlite3.Connection):
    response = interactors.handle_user(conn, "/user rm 69")

    assert response == "Пользователь 69 удален"


def test_correct_ls_user(conn: sqlite3.Connection):
    repository.create_user(conn, 69)

    response = interactors.handle_user(conn, "/user ls")

    assert response == "Список id:\n`69`"


def test_print_usage(conn: sqlite3.Connection):
    usage = (
        "`/user add` id \\- добавить пользователя по id\n"
        "`/user rm` id \\- удалить пользователя по id\n"
        "`/user ls` \\- список id пользователей"
    )

    response = interactors.handle_user(conn, "/user")

    assert response == usage


def test_error_print_usage(conn: sqlite3.Connection):
    usage = (
        "`/user add` id \\- добавить пользователя по id\n"
        "`/user rm` id \\- удалить пользователя по id\n"
        "`/user ls` \\- список id пользователей"
    )

    response = interactors.handle_user(conn, "/user dd 69")

    assert response == f"Неизвестная команда dd\n\n{usage}"
