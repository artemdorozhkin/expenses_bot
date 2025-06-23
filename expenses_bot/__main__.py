import os

from dotenv import load_dotenv

load_dotenv()


from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)

from expenses_bot.infrastructure import db
from expenses_bot.infrastructure.handlers import (
    category_handler,
    expense_handler,
    user_handler,
)
from expenses_bot.core import config


def main():
    token = os.getenv("TOKEN")
    if not token:
        raise ValueError("env variable TOKEN is required")

    with db.session(config.DB_FILE) as conn:
        db.init(conn)

    bot = Application.builder().token(token=token).build()

    bot.add_handler(CommandHandler(command="user", callback=user_handler.user))
    bot.add_handler(
        CommandHandler(command="category", callback=category_handler.category)
    )

    bot.add_handler(
        CallbackQueryHandler(category_handler.add_query, pattern="^add_category:.*")
    )

    bot.add_handler(MessageHandler(filters.TEXT, expense_handler.parse_expense))

    bot.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
