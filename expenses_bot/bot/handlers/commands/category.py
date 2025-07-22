import logging
from telegram import Update
from telegram.ext import ContextTypes

from expenses_bot import config, db
from expenses_bot.bot.decorators import only_users
from expenses_bot.core import category

log = logging.getLogger(__name__)


@only_users
async def run(update: Update, _: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    user_id = update.effective_user.id if update.effective_user else "unknown"

    if not msg:
        log.warning(f"No message object received from user {user_id}")
        return

    log.info(f"Listing categories for user {user_id}")

    with db.session(config.DB_FILE) as conn:
        response = category.list(conn)

    await msg.reply_markdown_v2(response)
    log.debug(f"Sent category list to user {user_id}")
