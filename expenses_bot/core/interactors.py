import sqlite3

from telegram import InlineKeyboardMarkup

from expenses_bot.core import messages, parser, validators
from expenses_bot.core import keyboards


def handle_expanse_input(
    conn: sqlite3.Connection, user_input: str
) -> tuple[str, InlineKeyboardMarkup | None]:
    try:
        expenses = parser.parse_expenses(user_input=user_input)
    except ValueError:
        return (
            "Не удалось получить данные о расходах\\. Необходимо прислать сообщение в формате:\n`69 категория`",
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
                f"Не удалось найти категорию *{e.category}*\\.\nВозможно имелась ввиду категория *{guess}*?",
                keyboards.choose_category(add_new_name=e.category, guessed_name=guess),
            )

        if guess and guess.lower() == e.category.lower():
            e.category = guess

    return messages.create_confirm_message(expenses=expenses), keyboards.add_expense()
