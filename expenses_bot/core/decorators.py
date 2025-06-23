from functools import wraps
import os

from telegram import Update
from telegram.ext import ContextTypes

from expenses_bot.core import config
from expenses_bot.infrastructure import db, repository


async def not_allowed(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    if not msg:
        return

    await context.bot.send_message(
        chat_id=int(os.getenv("ADMIN")),
        text=f"{msg.from_user.id=}",
    )
    await msg.reply_markdown_v2("*Доступ запрещен*")


def only_admin(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        update: Update | None = None
        if args:
            update = args[0]
        else:
            update = kwargs.get("update")

        if update and update.message and update.message.from_user:
            sender_id = update.message.from_user.id
            if isinstance(sender_id, int) and sender_id == int(os.getenv("ADMIN")):
                return func(*args, **kwargs)

        return not_allowed(*args, **kwargs)

    return wrapper


def only_users(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        update: Update | None = None
        if args:
            update = args[0]
        else:
            update = kwargs.get("update")

        if update and update.message and update.message.from_user:
            sender_id = update.message.from_user.id
            with db.session(config.DB_FILE) as conn:
                users = repository.get_all_users(conn)
                users.append(int(os.getenv("ADMIN")))

            if isinstance(sender_id, int) and sender_id in users:
                return func(*args, **kwargs)

        return not_allowed(*args, **kwargs)

    return wrapper
