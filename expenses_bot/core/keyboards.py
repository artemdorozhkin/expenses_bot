from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def add_category(name: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=f"Добавить: {name}",
                    callback_data=f"add_category:{name}",
                )
            ]
        ]
    )


def choose_category(add_new_name: str, guessed_name: str) -> InlineKeyboardMarkup:
    buttons: list[tuple[str, str]] = [
        {
            "text": f"Добавить: {add_new_name}",
            "data": f"add_category:{add_new_name}",
        },
        {
            "text": f"Выбрать: {guessed_name}",
            "data": f"choose_category:{guessed_name}",
        },
    ]
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=button["text"],
                    callback_data=button["data"],
                )
            ]
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
