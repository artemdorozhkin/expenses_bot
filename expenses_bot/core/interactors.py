import sqlite3
from expenses_bot.core import messages, parser, validators, config
from expenses_bot.infrastructure import db


def handle_expanse_input(conn: sqlite3.Connection, user_input: str) -> str:
    try:
        expenses = parser.parse_expenses(user_input=user_input)
    except ValueError:
        return "Не удалось получить данные о расходах\\. Необходимо прислать сообщение в формате:\n`69 категория`"

    for e in expenses:
        guess = validators.validate_category(conn=conn, name=e.category)
        if not guess:
            return f"Не удалось найти категорию *{e.category}*\\.\nДобавить?"

        if guess and guess.lower() != e.category.lower():
            return f"Не удалось найти категорию *{e.category}*\\.\nВозможно имелась ввиду категория *{guess}*?"

        if guess and guess.lower() == e.category.lower():
            e.category = guess

    return messages.create_confirm_message(expenses=expenses)
