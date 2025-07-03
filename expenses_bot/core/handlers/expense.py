from datetime import datetime, timedelta, timezone
import sqlite3
from typing import Literal
from expenses_bot.core import parser
from expenses_bot.core.models import Expense
from expenses_bot.infrastructure import repository


def handle(
    conn: sqlite3.Connection | None,
    user_id: int,
    user_input: str | Literal["today", "week", "month"],
) -> tuple[Expense, ...]:
    if user_input in ("today", "week", "month") and conn:
        if user_input == "today":
            starts_date = datetime.now(timezone.utc).date()
            expenses = repository.get_expenses_starts_with_date(
                conn, starts_date, user_id
            )
        elif user_input == "week":
            starts_date = (datetime.now(timezone.utc) - timedelta(days=7)).date()
            expenses = repository.get_expenses_starts_with_date(
                conn, starts_date, user_id
            )
        elif user_input == "month":
            starts_date = datetime.now(timezone.utc).date().replace(day=1)
            expenses = repository.get_expenses_starts_with_date(
                conn, starts_date, user_id
            )
        else:
            raise ValueError(f"Не удалось обработать период {user_input}")

        return tuple(expenses)

    try:
        expenses = parser.parse_expenses(user_input=user_input)
    except ValueError as e:
        raise ValueError(
            (
                "Не удалось получить данные о расходах\\. "
                "Необходимо прислать сообщение в формате:\n`69 категория`"
            )
        ) from e

    return expenses
