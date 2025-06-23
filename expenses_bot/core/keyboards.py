from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def add_category(name: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=f"Добавить: {name}",
                    callback_data="add_category",
                )
            ]
        ]
    )


def choose_category(add_new_name: str, guessed_name: str) -> InlineKeyboardMarkup:
    buttons: list[tuple[str, str]] = [
        (f"Добавить: {add_new_name}", "add_category"),
        (f"Выбрать: {guessed_name}", "choose_category"),
    ]
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(text=button[0], callback_data=button[1])]
            for button in buttons
        ]
    )


def add_expense() -> InlineKeyboardMarkup:
    buttons: list[tuple[str, str]] = [
        ("Добавить расход", "add_expense"),
        ("Изменить категорию", "edit_category"),
        ("Изменить сумму", "edit_amount"),
        ("Изменить дату", "edit_date"),
    ]
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(text=button[0], callback_data=button[1])]
            for button in buttons
        ]
    )
