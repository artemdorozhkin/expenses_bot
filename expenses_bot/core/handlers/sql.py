import sqlite3
from tabulate import tabulate


def handle(conn: sqlite3.Connection, query: str) -> str:
    try:
        cursor = conn.execute(query)
    except sqlite3.Error as e:
        return str(e)

    if "select" in query.lower():
        response = cursor.fetchall()
        text = tabulate(response, headers=[d[0] for d in cursor.description])
        result = []
        for line in text.split("\n"):
            result.append(f"`{line}`")
        return "\n".join(result)

    return "Выполнено"
