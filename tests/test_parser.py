from datetime import datetime
import pytest

from expenses_bot.core import parser
from expenses_bot.core.models import Expense


def test_one_correct_expense():
    user_input = "69 продукты"
    current_date = datetime.now().date()

    result = parser.parse_expenses(user_input)

    assert len(result) == 1
    assert result[0] == Expense(
        category="продукты",
        amount=69.0,
        created_at=current_date,
    )


def test_two_correct_expense():
    user_input = "69 продукты\nбытовая химия 42.69"
    current_date = datetime.now().date()

    result = parser.parse_expenses(user_input)

    assert len(result) == 2
    assert result[0] == Expense(
        category="продукты",
        amount=69.0,
        created_at=current_date,
    )

    assert result[1] == Expense(
        category="бытовая химия",
        amount=42.69,
        created_at=current_date,
    )


def test_incorrect_expense():
    user_input = "hello world"
    with pytest.raises(ValueError):
        _ = parser.parse_expenses(user_input)
