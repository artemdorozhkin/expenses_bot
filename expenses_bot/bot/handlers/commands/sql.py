from telegram import Update
from telegram.ext import ContextTypes

from expenses_bot import config
from expenses_bot.bot.decorators import only_admin
from expenses_bot.core import sql
from expenses_bot import db


@only_admin
async def run(update: Update, _: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    if not msg:
        return
    if not msg.text:
        return

    with db.session(config.DB_FILE) as conn:
        query = msg.text[5:]
        response = sql.execute(conn, query)
        if not response:
            await msg.reply_text("[]")
        else:
            await msg.reply_markdown_v2(response)
