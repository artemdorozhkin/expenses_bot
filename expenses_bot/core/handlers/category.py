import sqlite3

from expenses_bot.infrastructure import repository


def handle(conn: sqlite3.Connection, user_id: int, name: str | None = None) -> str:
    if name:
        repository.create_category(conn, name, user_id)
        return f"Добавлена категория: {name}"

    categories = repository.get_all_categories(conn, user_id)
    if len(categories) == 0:
        return "Категории еще не добавлены"

    return f"*ДОБАВЛЕННЫЕ КАТЕГОРИИ*\n\n{'\n'.join([c.name for c in categories])}"
