import os

from dotenv import load_dotenv

load_dotenv()

from telegram import Update
from telegram.ext import Application, MessageHandler, filters

from expenses_bot.infrastructure import handlers


def main():
    token = os.getenv("TOKEN")
    if not token:
        raise ValueError("env variable TOKEN is required")

    bot = Application.builder().token(token=token).build()
    bot.add_handler(MessageHandler(filters.TEXT, handlers.parse_expense))

    bot.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
