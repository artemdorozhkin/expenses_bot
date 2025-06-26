from telegram.ext import (
    CallbackQueryHandler,
    MessageHandler,
    filters,
)

from expenses_bot.infrastructure.dialogs import expense

expense_dialog = [
    MessageHandler(callback=expense.start, filters=filters.TEXT),
    CallbackQueryHandler(expense.add_category_query, pattern="^add_category:.*"),
    CallbackQueryHandler(expense.choose_category_query, pattern="^choose_category:.*"),
    CallbackQueryHandler(expense.add_expenses_query, pattern="add_expenses"),
    CallbackQueryHandler(expense.cancel, pattern="cancel_add_expenses"),
]
