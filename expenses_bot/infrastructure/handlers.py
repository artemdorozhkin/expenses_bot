import os
from telegram import Update
from telegram.ext import ContextTypes

from expenses_bot.core import config, interactors
from expenses_bot.core.decorators import only_admin
from expenses_bot.infrastructure import db


async def not_allowed(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    if not msg:
        return None

    await context.bot.send_message(
        chat_id=int(os.getenv("ADMIN")),
        text=f"{msg.from_user.id=}",
    )
    await msg.reply_markdown_v2("*Доступ запрещен*")


@only_admin
async def add_user(update: Update, _: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    if not msg:
        return None

    if not msg.text:
        return None

    with db.session(config.DB_FILE) as conn:
        response = interactors.handle_add_user(conn, msg.text)
    await msg.reply_text(response)


@only_admin
async def parse_expense(update: Update, _: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    if not msg:
        return None

    if not msg.text:
        return None

    with db.session(config.DB_FILE) as conn:
        text, keyboard = interactors.handle_expanse_input(conn, msg.text)
        await msg.reply_markdown_v2(text=text, reply_markup=keyboard)
