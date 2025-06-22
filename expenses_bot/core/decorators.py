from functools import wraps
import os

from telegram import Message, Update, User

from expenses_bot.infrastructure import handlers


def only_admin(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        update: Update | None = None
        if args:
            update = args[0]
        else:
            update = kwargs.get("mid")

        if not update:
            return handlers.not_allowed(*args, **kwargs)

        msg = update.message
        if not msg:
            return handlers.not_allowed(*args, **kwargs)

        sender = msg.from_user
        if not sender:
            return handlers.not_allowed(*args, **kwargs)

        if isinstance(sender.id, int) and sender.id in map(
            int, os.getenv("USERS").split(",")
        ):
            return func(*args, **kwargs)
        return handlers.not_allowed(*args, **kwargs)

    return wrapper
