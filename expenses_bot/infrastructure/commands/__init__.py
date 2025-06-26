from telegram.ext import CommandHandler

from expenses_bot.infrastructure.commands import category, user

user_cmd = CommandHandler(command="user", callback=user.run)
category_cmd = CommandHandler(command="category", callback=category.run)
