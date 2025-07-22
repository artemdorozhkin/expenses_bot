import os

from dotenv import load_dotenv

load_dotenv()

from telegram import Update
from telegram.ext import Application

from expenses_bot import db, config, logger
from expenses_bot.bot import dispatcher


log = logger.setup_logger()


def main():
    token = os.getenv("TOKEN")
    if not token:
        raise ValueError("Env variable TOKEN is required")

    log.info("DB initialization...")
    with db.session(config.DB_FILE) as conn:
        db.init(conn)

    log.info("Starting bot...")
    bot = Application.builder().token(token=token).build()
    dispatcher.register_handlers(bot)

    bot.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        log.critical(e)
