from datetime import datetime
from expenses_bot import messages
from expenses_bot.models import Expense


def test_cteate_one_expense_confirm():
    current_date = datetime.now().date()
    expense = Expense(
        category="Продукты",
        amount=69.0,
        created_at=current_date,
    )

    text = messages.create_confirm_message([expense])

    assert (
        text
        == """Категория: Продукты
Сумма: 69.0

Дата: {}""".format(
            current_date.strftime("%d.%m.%Y")
        )
    )


def test_cteate_two_expense_confirm():
    current_date = datetime.now().date()
    expenses = [
        Expense(
            category="Продукты",
            amount=69.0,
            created_at=current_date,
        ),
        Expense(
            category="Бытовая химия",
            amount=42.69,
            created_at=current_date,
        ),
    ]

    text = messages.create_confirm_message(expenses)

    assert (
        text
        == """Категория: Продукты
Сумма: 69.0
Категория: Бытовая химия
Сумма: 42.69

Дата: {}""".format(
            current_date.strftime("%d.%m.%Y")
        )
    )


def test_guessed_category():
    original_name = "Продуктовый"
    guessed_name = "Продукты"

    text = messages.create_not_guess_category_message(original_name, guessed_name)

    assert (
        text
        == f"Не удалось найти категорию '{original_name}'.\nВозможно имелась ввиду: '{guessed_name}'"
    )


def test_not_guessed_category():
    original_name = "Продуктовый"

    text = messages.create_not_guess_category_message(original_name, None)

    assert (
        text == f"Не удалось найти категорию '{original_name}'.\nХотите создать новую?"
    )
