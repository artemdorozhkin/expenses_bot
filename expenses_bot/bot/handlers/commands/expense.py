import logging
from typing import cast
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from expenses_bot import config, db
from expenses_bot.bot import messages, keyboards
from expenses_bot.bot.decorators import only_users
from expenses_bot.core import expense

log = logging.getLogger(__name__)


@only_users
async def run(update: Update, _: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id if update.effective_user else "unknown"
    msg = update.message

    if not (msg and msg.text):
        log.warning("Empty or non-text message received | user_id=%s", user_id)
        return

    log.info("Expense period keyboard requested | user_id=%s", user_id)

    keyboard = keyboards.get_periods()
    await msg.reply_markdown_v2("Выберите период", reply_markup=keyboard)

    log.debug("Period keyboard sent | user_id=%s", user_id)


async def show_expenses_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    callback = update.callback_query
    user_id = callback.from_user.id if callback else "unknown"

    if not (callback and callback.data):
        log.warning("Callback query without data | user_id=%s", user_id)
        return

    period = callback.data.strip("_expenses")
    log.info("Expense report requested | user_id=%s | period=%s", user_id, period)
    with db.session(config.DB_FILE) as conn:
        await callback.delete_message()
        try:
            response = expense.get_expenses_by_period(
                conn,
                cast(expense.Period, period),
            )
        except ValueError as e:
            log.error(
                "Invalid period or parse error | user_id=%s | err=%s",
                user_id,
                e,
            )
            return await context.bot.send_message(
                chat_id=callback.from_user.id, text=str(e)
            )

        period_names = {"today": "сегодня", "week": "неделю", "month": "текущий месяц"}
        text = messages.create_expenses_report(response)
        text = f"*СТАТИСТИКА РАСХОДОВ ЗА {period_names[period].upper()}*\n\n{text}"
        await context.bot.send_message(
            chat_id=callback.from_user.id,
            text=text,
            parse_mode=ParseMode.MARKDOWN_V2,
        )

        log.debug("Expense report sent | user_id=%s | period=%s", user_id, period)
