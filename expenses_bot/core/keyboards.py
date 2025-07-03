from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def _make_markup(*buttons: dict[str, str]) -> InlineKeyboardMarkup:
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


def add_category(name: str) -> InlineKeyboardMarkup:
    button = {"text": f"Добавить: {name}", "data": f"add_category:{name}"}
    return _make_markup(button)


def choose_category(add_new_name: str, guessed_name: str) -> InlineKeyboardMarkup:
    buttons = [
        {
            "text": f"Добавить: {add_new_name}",
            "data": f"add_category:{add_new_name}",
        },
        {
            "text": f"Выбрать: {guessed_name}",
            "data": f"choose_category:{guessed_name}",
        },
    ]
    return _make_markup(*buttons)


def add_expense(on_add_index: int) -> InlineKeyboardMarkup:
    buttons = [
        {
            "text": "Добавить расходы",
            "data": f"add_expenses:{on_add_index}",
        },
        {
            "text": "Отмена",
            "data": f"cancel_add_expenses:{on_add_index}",
        },
    ]
    return _make_markup(*buttons)


def get_periods() -> InlineKeyboardMarkup:
    buttons = [
        {
            "text": "За сегодня",
            "data": "today_expenses",
        },
        {
            "text": "За неделю",
            "data": "week_expenses",
        },
        {
            "text": "За текущий месяц",
            "data": "month_expenses",
        },
        {
            "text": "Отмена",
            "data": "cancel_select_periods",
        },
    ]
    return _make_markup(*buttons)
