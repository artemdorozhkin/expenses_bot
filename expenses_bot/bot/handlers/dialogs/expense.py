from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from expenses_bot import config, db
from expenses_bot.bot import keyboards, messages
from expenses_bot.bot.decorators import only_users
from expenses_bot.core import validators, expense as expense_handler, category
from expenses_bot.db import repository
from expenses_bot.db.models import Expense


@only_users
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message

    if msg and msg.text:
        try:
            context.user_data["expenses"] = expense_handler.parse_expenses_from_input(
                msg.text
            )
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
    if not context.user_data:
        return

    expenses: tuple[Expense, ...] = context.user_data.get("expenses", tuple())
    eid = context.user_data.get("eid", -1)

    if len(expenses) == 0 or eid == -1:
        return

    if len(expenses) <= eid:
        await show_summary(update, context)
        return

    with db.session(config.DB_FILE) as conn:
        is_valid, guessed_name = validators.validate_category(
            conn, expenses[eid].category
        )
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
    if not context.user_data:
        return

    msg = update.message
    bot = context.bot

    expenses: tuple[Expense, ...] = context.user_data.get("expenses", tuple())
    on_add_index: int = context.user_data.get("on_add_index", 0) or 0
    context.user_data["on_add_index"] = on_add_index + 1
    on_add: dict[int, tuple[Expense, ...]] = context.user_data.get("on_add", {}) or {}
    on_add[on_add_index] = expenses
    context.user_data["on_add"] = on_add

    text = messages.create_confirm_message(expenses)
    kb = keyboards.add_expense(on_add_index)

    if msg:
        await msg.reply_markdown_v2(text, reply_markup=kb)
    else:
        callback = update.callback_query
        if not callback:
            return

        await callback.delete_message()
        await bot.send_message(
            chat_id=callback.from_user.id,
            text=text,
            reply_markup=kb,
            parse_mode=ParseMode.MARKDOWN_V2,
        )


async def add_category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data:
        return

    msg = update.message
    bot = context.bot

    expenses: tuple[Expense, ...] = context.user_data.get("expenses", tuple())
    eid = context.user_data.get("eid", -1)
    expense = expenses[eid]

    text = messages.create_not_guess_category_message(expense.category)
    kb = keyboards.add_category(expense.category)

    if msg:
        await msg.reply_markdown_v2(text, reply_markup=kb)
    else:
        callback = update.callback_query
        if not callback:
            return

        await callback.delete_message()
        await bot.send_message(
            chat_id=callback.from_user.id,
            text=text,
            reply_markup=kb,
            parse_mode=ParseMode.MARKDOWN_V2,
        )


async def choose_category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data:
        return

    msg = update.message
    bot = context.bot

    expenses: tuple[Expense, ...] = context.user_data.get("expenses", tuple())
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
        if not callback:
            return

        await callback.delete_message()
        await bot.send_message(
            chat_id=callback.from_user.id,
            text=text,
            reply_markup=kb,
            parse_mode=ParseMode.MARKDOWN_V2,
        )


async def add_category_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    callback = update.callback_query
    if not callback:
        return
    if not callback.data:
        return
    if not context.user_data:
        return

    with db.session(config.DB_FILE) as conn:
        expenses: tuple[Expense, ...] = context.user_data.get("expenses", tuple())
        eid = context.user_data.get("eid", -1)

        _, name = callback.data.split(":")
        expenses[eid].category = name
        context.user_data["eid"] += 1
        context.user_data["expenses"] = expenses

        category.add(conn, name=name)
        conn.commit()

        await callback.answer()
        await confirm_categories(update, context)


async def choose_category_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    callback = update.callback_query
    if not callback:
        return
    if not callback.data:
        return
    if not context.user_data:
        return

    with db.session(config.DB_FILE) as conn:
        expenses: tuple[Expense, ...] = context.user_data.get("expenses", tuple())
        eid = context.user_data.get("eid", -1)

        _, name = callback.data.split(":")
        expenses[eid].category = name
        context.user_data["eid"] += 1
        context.user_data["expenses"] = expenses

        await callback.answer()
        await confirm_categories(update, context)


async def add_expenses_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    callback = update.callback_query
    if not callback:
        return
    if not callback.data:
        return
    if not context.user_data:
        return

    with db.session(config.DB_FILE) as conn:
        on_add_index: int = int(callback.data.split(":")[-1])
        on_add: dict[int, tuple[Expense, ...]] = context.user_data.get("on_add", {})
        expenses: tuple[Expense, ...] = on_add.pop(on_add_index, tuple())

        if len(on_add) == 0:
            context.user_data["on_add"] = None
            context.user_data["on_add_index"] = None
        else:
            context.user_data["on_add"] = on_add

        repository.create_expenses(conn, expenses)

        await callback.answer()
        await callback.delete_message()
        text = messages.create_expenses_successfully_added(expenses)
        await context.bot.send_message(
            chat_id=callback.from_user.id,
            text=text,
            parse_mode=ParseMode.MARKDOWN_V2,
        )


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    callback = update.callback_query
    bot = context.bot
    if not callback:
        return
    if not callback.data:
        return
    if not context.user_data:
        return

    with db.session(config.DB_FILE) as conn:
        on_add_index: int = int(callback.data.split(":")[-1])
        on_add: dict[int, tuple[Expense, ...]] = context.user_data.get("on_add", {})
        on_add.pop(on_add_index)
        if len(on_add) == 0:
            context.user_data["on_add"] = None
            context.user_data["on_add_index"] = None
        else:
            context.user_data["on_add"] = on_add

        await callback.answer()
        await callback.delete_message()
        await bot.send_message(
            text="Добавление расхода отменено",
            chat_id=callback.from_user.id,
        )
