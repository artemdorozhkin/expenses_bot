from datetime import datetime, timedelta, timezone
import sqlite3
from typing import Literal

from expenses_bot.core import parser
from expenses_bot.db.models import Expense
from expenses_bot.db import repository

Period = Literal["today", "week", "month"]


def parse_expenses_from_input(user_input: str) -> tuple[Expense, ...]:
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


from datetime import datetime, timedelta, timezone
import sqlite3


def get_expenses_by_period(conn: sqlite3.Connection, period: Period) -> tuple:
    if not conn:
        raise ValueError("Нет соединения с базой")

    now = datetime.now(timezone.utc)

    if period == "today":
        start_date = now.date()
    elif period == "week":
        start_date = (now - timedelta(days=7)).date()
    elif period == "month":
        start_date = now.date().replace(day=1)
    else:
        raise ValueError(f"Неверный период: {period}")

    expenses = repository.get_expenses_starts_with_date(conn, start_date)
    return tuple(expenses)
