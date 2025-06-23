from telegram import Update
from telegram.ext import ContextTypes

from expenses_bot.core import config, interactors
from expenses_bot.core.decorators import only_admin
from expenses_bot.infrastructure import db


async def not_allowed(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    if not msg:
        return None

    if not msg.text:
        return None

    await msg.reply_markdown_v2("*Доступ запрещен*")


@only_admin
async def parse_expense(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    if not msg:
        return None

    if not msg.text:
        return None

    with db.session(config.DB_FILE) as conn:
        text, keyboard = interactors.handle_expanse_input(conn, msg.text)
        await msg.reply_markdown_v2(text=text, reply_markup=keyboard)
