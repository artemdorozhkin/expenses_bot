from telegram.ext import CommandHandler, CallbackQueryHandler

from expenses_bot.bot.handlers.commands import category, sql, user, expense

user_cmd = CommandHandler(command="user", callback=user.run)
category_cmd = CommandHandler(command="category", callback=category.run)
expense_cmd_dialog = [
    CommandHandler(command="expense", callback=expense.run),
    CallbackQueryHandler(
        expense.show_expenses_query, pattern="(today|week|month)_expenses"
    ),
]

sql_cmd = CommandHandler(command="sql", callback=sql.run)
