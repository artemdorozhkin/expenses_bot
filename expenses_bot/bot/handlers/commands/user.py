from telegram import Update
from telegram.ext import ContextTypes

from expenses_bot import config, db
from expenses_bot.bot.decorators import only_admin
from expenses_bot.core import user


@only_admin
async def run(update: Update, _: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    if msg and msg.text:
        with db.session(config.DB_FILE) as conn:
            try:
                response = user.execute(conn, msg.text)
            except ValueError as e:
                response = f"{e}\n\n{user.USAGE}"
        await msg.reply_markdown_v2(response)
