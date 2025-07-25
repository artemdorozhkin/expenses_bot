import sqlite3
import difflib

from expenses_bot.db import repository


def validate_category(conn: sqlite3.Connection, name: str) -> tuple[bool, str | None]:
    categories = repository.get_all_categories(conn)
    names = [c.name for c in categories]

    for n in names:
        if name.lower() in n.lower():
            return True, n

    matches = difflib.get_close_matches(name, names, n=1, cutoff=0.65)
    return False, matches[0] if matches else None
