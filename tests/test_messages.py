from datetime import datetime
from expenses_bot.core import messages
from expenses_bot.core.models import Expense


def test_cteate_one_expense_confirm():
    current_date = datetime.now().date()
    expense = Expense(
        category="Продукты",
        amount=69.0,
        created_at=current_date,
    )

    text = messages.create_confirm_message((expense,))

    assert (
        text
        == """Категория: Продукты
Сумма: 69\\.0

Дата: {}""".format(
            current_date.strftime("%d\\.%m\\.%Y")
        )
    )


def test_cteate_two_expense_confirm():
    current_date = datetime.now().date()
    expenses = (
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
    )

    text = messages.create_confirm_message(expenses)

    assert (
        text
        == """Категория: Продукты
Сумма: 69\\.0
Категория: Бытовая химия
Сумма: 42\\.69

Дата: {}""".format(
            current_date.strftime("%d\\.%m\\.%Y")
        )
    )


def test_guessed_category():
    original_name = "Продуктовый"
    guessed_name = "Продукты"

    text = messages.create_not_guess_category_message(original_name, guessed_name)

    assert (
        text
        == f"Не удалось найти категорию '{original_name}'\\.\nВозможно имелась ввиду: '{guessed_name}'"
    )


def test_not_guessed_category():
    original_name = "Продуктовый"

    text = messages.create_not_guess_category_message(original_name, None)

    assert (
        text
        == f"Не удалось найти категорию '{original_name}'\\.\nХотите создать новую?"
    )


def test_cteate_expenses_report():
    current_date = datetime.now().date()
    expenses = (
        Expense(
            category="Продукты",
            amount=34.0,
            created_at=current_date,
        ),
        Expense(
            category="Продукты",
            amount=35.0,
            created_at=current_date,
        ),
        Expense(
            category="Бытовая химия",
            amount=42.69,
            created_at=current_date,
        ),
    )

    text = messages.create_expenses_report(expenses)

    assert (
        text
        == """`Продукты                 : 69\\.00`
`Бытовая химия            : 42\\.69`

`Общая сумма за период    : 111\\.69`"""
    )


def test_create_expenses_successfully_added():
    current_date = datetime.now().date()
    expenses = (
        Expense(
            category="Продукты",
            amount=34.0,
            created_at=current_date,
        ),
        Expense(
            category="Продукты",
            amount=35.0,
            created_at=current_date,
        ),
        Expense(
            category="Бытовая химия",
            amount=42.69,
            created_at=current_date,
        ),
    )

    text = messages.create_expenses_successfully_added(expenses)

    assert (
        text
        == """*РАСХОДЫ УСПЕШНО ДОБАВЛЕНЫ*

`Продукты                 : 34\\.00`
`Продукты                 : 35\\.00`
`Бытовая химия            : 42\\.69`
"""
    )
