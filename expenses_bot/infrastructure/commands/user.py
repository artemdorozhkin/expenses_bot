from telegram import Update
from telegram.ext import ContextTypes

from expenses_bot.core import config
from expenses_bot.core.decorators import only_admin
from expenses_bot.core.handlers import user
from expenses_bot.infrastructure import db


@only_admin
async def run(update: Update, _: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    if msg and msg.text:
        with db.session(config.DB_FILE) as conn:
            response = user.handle(conn, msg.text)
        await msg.reply_markdown_v2(response)
