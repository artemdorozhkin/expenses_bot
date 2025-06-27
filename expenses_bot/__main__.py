import os

from dotenv import load_dotenv

load_dotenv()

from telegram import Update
from telegram.ext import Application

from expenses_bot.infrastructure.dialogs import expense_dialog
from expenses_bot.infrastructure import db
from expenses_bot.infrastructure.commands import (
    category_cmd,
    user_cmd,
    expense_cmd_dialog,
)
from expenses_bot.core import config


def main():
    token = os.getenv("TOKEN")
    if not token:
        raise ValueError("env variable TOKEN is required")

    with db.session(config.DB_FILE) as conn:
        db.init(conn)

    bot = Application.builder().token(token=token).build()

    bot.add_handler(user_cmd)
    bot.add_handler(category_cmd)
    bot.add_handlers(expense_cmd_dialog)
    bot.add_handlers(expense_dialog)

    bot.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
