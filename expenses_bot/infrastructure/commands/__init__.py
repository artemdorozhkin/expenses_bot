from telegram.ext import CommandHandler, CallbackQueryHandler

from expenses_bot.infrastructure.commands import category, user, expense

user_cmd = CommandHandler(command="user", callback=user.run)
category_cmd = CommandHandler(command="category", callback=category.run)
expense_cmd_dialog = [
    CommandHandler(command="expense", callback=expense.run),
    CallbackQueryHandler(
        expense.show_expenses_query, pattern="(today|week|month)_expenses"
    ),
]
