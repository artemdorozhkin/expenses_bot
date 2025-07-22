from typing import cast
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from expenses_bot import config, db
from expenses_bot.bot import messages, keyboards
from expenses_bot.bot.decorators import only_users
from expenses_bot.core import expense


@only_users
async def run(update: Update, _: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    if msg and msg.text:
        text = "Выберите период"
        keyboard = keyboards.get_periods()

        await msg.reply_markdown_v2(text, reply_markup=keyboard)


async def show_expenses_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    callback = update.callback_query
    if callback and callback.data:
        period_names = {"today": "сегодня", "week": "неделю", "month": "текущий месяц"}
        period = callback.data.strip("_expenses")
        with db.session(config.DB_FILE) as conn:
            await callback.delete_message()
            try:
                response = expense.get_expenses_by_period(
                    conn,
                    cast(expense.Period, period),
                )
            except ValueError as e:
                return await context.bot.send_message(
                    chat_id=callback.from_user.id, text=str(e)
                )

            text = messages.create_expenses_report(response)
            text = f"*СТАТИСТИКА РАСХОДОВ ЗА {period_names[period].upper()}*\n\n{text}"
            await context.bot.send_message(
                chat_id=callback.from_user.id,
                text=text,
                parse_mode=ParseMode.MARKDOWN_V2,
            )
