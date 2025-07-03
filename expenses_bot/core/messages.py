from expenses_bot.core.models import Expense


def create_confirm_message(expenses: tuple[Expense, ...]) -> str:
    agregated: dict[str, float] = {}
    for e in expenses:
        if e.category in agregated:
            agregated[e.category] += e.amount
        else:
            agregated[e.category] = e.amount

    text = ""
    for category, amount in agregated.items():
        text += f"Категория: {category}\nСумма: {str(amount).replace('.', '\\.')}\n"

    return f"{text}\nДата: {expenses[0].created_at.strftime("%d\\.%m\\.%Y")}"


def create_not_guess_category_message(
    original_name: str,
    guessed_name: str | None = None,
) -> str:
    if guessed_name:
        return f"Не удалось найти категорию '{original_name}'\\.\nВозможно имелась ввиду: '{guessed_name}'"

    return f"Не удалось найти категорию '{original_name}'\\.\nХотите создать новую?"


def create_expenses_report(expenses: tuple[Expense, ...]) -> str:
    total_amount: float = 0
    agregated: dict[str, float] = {}
    for e in expenses:
        total_amount += e.amount
        if e.category in agregated:
            agregated[e.category] += e.amount
        else:
            agregated[e.category] = e.amount

    text = ""
    for category, amount in agregated.items():
        str_amount = f"{amount:.2f}".replace(".", "\\.")
        text += f"`{category:<25}: {str_amount}`\n"

    str_total = f"{total_amount:.2f}".replace(".", "\\.")
    text += f"\n`{'Общая сумма за период':<25}: {str_total}`"
    return text


def create_expenses_successfully_added(expenses: tuple[Expense, ...]) -> str:
    text = "*РАСХОДЫ УСПЕШНО ДОБАВЛЕНЫ*\n\n"
    for e in expenses:
        str_amount = f"{e.amount:.2f}".replace(".", "\\.")
        text += f"`{e.category:<25}: {str_amount}`\n"

    return text
