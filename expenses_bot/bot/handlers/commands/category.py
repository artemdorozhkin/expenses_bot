from telegram import Update
from telegram.ext import ContextTypes

from expenses_bot import config, db
from expenses_bot.bot.decorators import only_users
from expenses_bot.core import category


@only_users
async def run(update: Update, _: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    if not msg:
        return

    with db.session(config.DB_FILE) as conn:
        response = category.list(conn)
    await msg.reply_markdown_v2(response)
