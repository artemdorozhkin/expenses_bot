from datetime import datetime
import sqlite3

import pytest

from expenses_bot.core.handlers import expense
from expenses_bot.core.models import Expense


def test_cant_parse_input():
    with pytest.raises(ValueError):
        _ = expense.handle("69")


def test_correct_parse_one_expense(conn: sqlite3.Connection):
    user_input = "69 продукты"
    current_date = datetime.now().date()
    expect = (Expense("продукты", 69, current_date),)

    response = expense.handle(user_input)

    assert response == expect


def test_correct_parse_two_expenses():
    user_input = "69 продукты\nбытовая химия 42.69"
    current_date = datetime.now().date()
    expect = (
        Expense("продукты", 69, current_date),
        Expense("бытовая химия", 42.69, current_date),
    )

    response = expense.handle(user_input)

    assert response == expect
