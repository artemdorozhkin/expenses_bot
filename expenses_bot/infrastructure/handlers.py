from telegram import Update
from telegram.ext import ContextTypes


async def parse_expense(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    if msg and msg.text:
        await msg.reply_text(msg.text)
