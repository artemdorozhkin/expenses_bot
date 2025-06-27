from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from expenses_bot.core import config, keyboards, messages, validators
from expenses_bot.core.decorators import only_users
from expenses_bot.core.handlers import expense as expense_handler
from expenses_bot.core.models import Expense
from expenses_bot.infrastructure import db


@only_users
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    if not msg:
        return

    if not msg.text:
        return

    try:
        context.user_data["expenses"] = tuple(expense_handler.handle(msg.text))
        context.user_data["eid"] = 0
        await confirm_categories(update, context)
    except ValueError:
        await msg.reply_markdown_v2(
            (
                "Не удалось получить данные о расходах\\. "
                "Необходимо прислать сообщение в формате:\n`69 категория`"
            )
        )


async def confirm_categories(update: Update, context: ContextTypes.DEFAULT_TYPE):
    expenses: tuple[Expense] = context.user_data.get("expenses", tuple())
    eid = context.user_data.get("eid", -1)

    if not expenses or eid == -1:
        return

    if len(expenses) <= eid:
        await show_summary(update, context)
        return

    expense = expenses[eid]
    with db.session(config.DB_FILE) as conn:
        is_valid, guessed_name = validators.validate_category(conn, expense.category)
        if is_valid:
            expenses[eid].category = guessed_name
            context.user_data["eid"] += 1
            await confirm_categories(update, context)
            return

        if guessed_name is None:
            await add_category(update, context)
            return

        context.user_data["guessed_category"] = guessed_name
        await choose_category(update, context)


async def show_summary(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    bot = context.bot

    expenses: tuple[Expense] = context.user_data.get("expenses", tuple())
    text = messages.create_confirm_message(expenses)
    kb = keyboards.add_expense()

    if msg:
        await msg.reply_markdown_v2(text, reply_markup=kb)
    else:
        callback = update.callback_query
        await callback.delete_message()
        await bot.send_message(
            chat_id=callback.from_user.id,
            text=text,
            reply_markup=kb,
            parse_mode=ParseMode.MARKDOWN_V2,
        )


async def add_category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    bot = context.bot

    expenses: tuple[Expense] = context.user_data.get("expenses", tuple())
    eid = context.user_data.get("eid", -1)
    expense = expenses[eid]

    text = messages.create_not_guess_category_message(expense.category)
    kb = keyboards.add_category(expense.category)

    if msg:
        await msg.reply_markdown_v2(text, reply_markup=kb)
    else:
        callback = update.callback_query
        await callback.delete_message()
        await bot.send_message(
            chat_id=callback.from_user.id,
            text=text,
            reply_markup=kb,
            parse_mode=ParseMode.MARKDOWN_V2,
        )


async def choose_category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    bot = context.bot

    expenses: tuple[Expense] = context.user_data.get("expenses", tuple())
    eid = context.user_data.get("eid", -1)
    expense = expenses[eid]
    guessed_name = context.user_data.get("guessed_category", None)
    if not guessed_name:
        return

    text = messages.create_not_guess_category_message(expense.category)
    kb = keyboards.choose_category(expense.category, guessed_name)

    if msg:
        await msg.reply_markdown_v2(text, reply_markup=kb)
    else:
        callback = update.callback_query
        await callback.delete_message()
        await bot.send_message(
            chat_id=callback.from_user.id,
            text=text,
            reply_markup=kb,
            parse_mode=ParseMode.MARKDOWN_V2,
        )
