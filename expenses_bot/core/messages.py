from expenses_bot.core.models import Expense


def create_confirm_message(expenses: list[Expense]) -> str:
    agregated: dict[str, float] = {}
    for e in expenses:
        if e.category in agregated:
            agregated[e.category] += e.amount
        else:
            agregated[e.category] = e.amount

    text = ""
    for category, amount in agregated.items():
        text += f"Категория: {category}\nСумма: {amount}\n"

    return f"{text}\nДата: {expenses[0].created_at.strftime("%d.%m.%Y")}"


def create_not_guess_category_message(
    original_name: str,
    guessed_name: str | None,
) -> str:
    if guessed_name:
        return f"Не удалось найти категорию '{original_name}'.\nВозможно имелась ввиду: '{guessed_name}'"

    return f"Не удалось найти категорию '{original_name}'.\nХотите создать новую?"
