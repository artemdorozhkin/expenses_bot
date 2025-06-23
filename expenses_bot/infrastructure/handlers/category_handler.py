from telegram import Update
from telegram.ext import ContextTypes

from expenses_bot.core import config
from expenses_bot.core.decorators import only_users
from expenses_bot.core.handlers import category_handler
from expenses_bot.core.models import Expense
from expenses_bot.infrastructure import db
from expenses_bot.infrastructure.handlers import expense_handler


@only_users
async def category(update: Update, _: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    if not msg:
        return

    with db.session(config.DB_FILE) as conn:
        response = category_handler.handle(conn)
    await msg.reply_markdown_v2(response)


async def add_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    callback = update.callback_query
    if not callback:
        return

    with db.session(config.DB_FILE) as conn:
        expenses: tuple[Expense] = context.user_data.get("expenses", tuple())
        eid = context.user_data.get("eid", -1)

        _, name = callback.data.split(":")
        expenses[eid].category = name
        context.user_data["eid"] += 1
        context.user_data["expenses"] = expenses

        category_handler.handle(conn, name=name)

        await callback.answer()
        await expense_handler.confirm_categories(update, context)


async def choose_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    callback = update.callback_query
    if not callback:
        return

    # with db.session(config.DB_FILE) as conn:
    #     expenses: tuple[Expense] = context.user_data.get("expenses", tuple())
    #     eid = context.user_data.get("eid", -1)

    #     context, name = callback.data.split(":")
    #     expenses[eid].category = name
    #     context.user_data["expenses"] = expenses

    #     category_handler.handle(conn, name=name)

    await callback.answer()
    await expense_handler.confirm_categories(update, context)
