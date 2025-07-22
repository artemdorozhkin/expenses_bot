from telegram.ext import Application

from expenses_bot.bot.handlers import dialogs, commands


def register_handlers(bot: Application):
    bot.add_handler(commands.user_cmd)
    bot.add_handler(commands.category_cmd)
    bot.add_handler(commands.sql_cmd)
    bot.add_handlers(commands.expense_cmd_dialog)
    bot.add_handlers(dialogs.expense_dialog)
