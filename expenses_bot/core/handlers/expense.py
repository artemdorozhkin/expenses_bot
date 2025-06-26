from expenses_bot.core import parser
from expenses_bot.core.models import Expense


def handle(user_input: str) -> tuple[Expense, ...]:
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
