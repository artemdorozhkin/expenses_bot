from telegram.ext import (
    CallbackQueryHandler,
    MessageHandler,
    filters,
)

from expenses_bot.infrastructure.dialogs import expense

expense_dialog = [
    MessageHandler(filters.TEXT, expense.start),
    CallbackQueryHandler(expense.add_query, pattern="^add_category:.*"),
    CallbackQueryHandler(expense.choose_query, pattern="^choose_category:.*"),
    CallbackQueryHandler(expense.add_expenses, pattern="add_expenses"),
]
