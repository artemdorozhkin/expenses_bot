import sqlite3

from expenses_bot.infrastructure import repository


def handle(conn: sqlite3.Connection) -> str:
    categories = repository.get_all_categories(conn)
    if len(categories) == 0:
        return "Категории еще не добавлены"

    return f"*ДОБАВЛЕННЫЕ КАТЕГОРИИ*:\n{'\n'.join([c.name for c in categories])}"
