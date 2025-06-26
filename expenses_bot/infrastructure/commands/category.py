from telegram import Update
from telegram.ext import ContextTypes

from expenses_bot.core import config
from expenses_bot.core.decorators import only_users
from expenses_bot.core.handlers import category
from expenses_bot.infrastructure import db


@only_users
async def run(update: Update, _: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    if not msg:
        return

    with db.session(config.DB_FILE) as conn:
        response = category.handle(conn)
    await msg.reply_markdown_v2(response)
