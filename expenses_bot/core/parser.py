from datetime import datetime

from expenses_bot.core.models import Expense


def parse_expenses(user_input: str) -> list[Expense]:
    """
    Parses user input into list of Expense's.

    user_input: str

    raises:
        ValueError when cant parse input
    """
    return [
        _parse_line_to_expense(line)
        for line in map(str.strip, user_input.splitlines())
        if line
    ]


def _parse_line_to_expense(line: str) -> Expense:
    parts = line.split(" ")
    current_date = datetime.now().date()

    for i in (0, -1):
        amount = _float_or_none(parts[i])
        if amount is not None:
            category = " ".join(parts[1:] if i == 0 else parts[:-1])
            return Expense(
                category=category,
                amount=amount,
                created_at=current_date,
            )

    raise ValueError(f"Incorrect input, can't parse '{line}'")


def _float_or_none(value: str) -> float | None:
    try:
        return float(value.replace(",", "."))
    except ValueError:
        return None
