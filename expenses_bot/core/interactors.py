import sqlite3
from typing import Literal

from telegram import InlineKeyboardMarkup

from expenses_bot.core import messages, parser, validators, keyboards
from expenses_bot.infrastructure import repository


def handle_expanse_input(
    conn: sqlite3.Connection,
    user_input: str,
) -> tuple[str, InlineKeyboardMarkup | None]:
    try:
        expenses = parser.parse_expenses(user_input=user_input)
    except ValueError:
        return (
            (
                "Не удалось получить данные о расходах\\. "
                "Необходимо прислать сообщение в формате:\n`69 категория`"
            ),
            None,
        )

    for e in expenses:
        guess = validators.validate_category(conn=conn, name=e.category)
        if not guess:
            return (
                f"Не удалось найти категорию *{e.category}*\\.\nДобавить?",
                keyboards.add_category(e.category),
            )

        if guess and guess.lower() != e.category.lower():
            return (
                (
                    f"Не удалось найти категорию *{e.category}*\\.\n"
                    f"Возможно имелась ввиду категория *{guess}*?"
                ),
                keyboards.choose_category(add_new_name=e.category, guessed_name=guess),
            )

        if guess and guess.lower() == e.category.lower():
            e.category = guess

    return messages.create_confirm_message(expenses=expenses), keyboards.add_expense()


def handle_user(conn: sqlite3.Connection, user_input: str) -> str:
    usage = (
        "`/user add` id \\- добавить пользователя по id\n"
        "`/user rm` id \\- удалить пользователя по id\n"
        "`/user ls` \\- список id пользователей"
    )
    args = user_input.split(" ")
    if len(args) == 1:
        return usage

    try:
        _, cmd, user_id = args
    except ValueError:
        try:
            _, cmd = args
            user_id = -1
        except ValueError:
            return f"Не корректно вызвана команда /user\n\n{usage}"

    try:
        response = _eval_user(conn, cmd, user_id)
    except ValueError as e:
        return f"{e}\n\n{usage}"

    return response


def _eval_user(
    conn: sqlite3.Connection,
    cmd: Literal["add", "rm", "ls"],
    user_id: int,
) -> str:
    commands = {
        "add": repository.create_user,
        "rm": repository.remove_user,
        "ls": repository.get_all_users,
    }
    if cmd not in commands:
        raise ValueError(f"Неизвестная команда {cmd}")

    command = commands[cmd]
    if cmd == "ls":
        users = command(conn)
        return f"Список id:\n{"\n".join([f'`{uid}`' for uid in users])}"

    command(conn, user_id)
    response = f"Пользователь {user_id} {'удален' if cmd == 'rm' else 'добавлен'}"

    return response
