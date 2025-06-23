from functools import wraps
import os

from telegram import Update

from expenses_bot.core import config
from expenses_bot.infrastructure import db, handlers, repository


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

        with db.session(config.DB_FILE) as conn:
            users = repository.get_all_users(conn)
        if isinstance(sender.id, int) and sender.id in (
            *users,
            int(os.getenv("ADMIN")),
        ):
            return func(*args, **kwargs)
        return handlers.not_allowed(*args, **kwargs)

    return wrapper
