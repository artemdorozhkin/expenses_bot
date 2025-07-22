import sqlite3

from expenses_bot.db import repository


def add(conn: sqlite3.Connection, name: str) -> str:
    repository.create_category(conn, name)
    return f"Добавлена категория: {name}"


def list(conn: sqlite3.Connection) -> str:
    categories = repository.get_all_categories(conn)
    if not categories:
        return "Категории еще не добавлены"
    return f"*ДОБАВЛЕННЫЕ КАТЕГОРИИ*\n\n{chr(10).join([c.name for c in categories])}"
