from dataclasses import dataclass
import sqlite3
from typing import Literal

from expenses_bot.db import repository

USAGE = (
    "`/user add` id \\- добавить пользователя по id\n"
    "`/user rm` id \\- удалить пользователя по id\n"
    "`/user ls` \\- список id пользователей"
)


@dataclass
class ParsedUserCommand:
    command: Literal["add", "rm", "ls"]
    user_id: int


def _parse_user_command(user_input: str) -> ParsedUserCommand:
    args = user_input.strip().split()
    if len(args) < 2:
        raise ValueError("Недостаточно аргументов")

    if args[0] != "/user":
        raise ValueError("Ожидалась команда /user")

    cmd = args[1]
    if cmd not in ("add", "rm", "ls"):
        raise ValueError(f"Неизвестная команда {cmd}")

    if cmd == "ls":
        return ParsedUserCommand(command=cmd, user_id=-1)

    if len(args) < 3:
        raise ValueError("Не указан ID пользователя")

    try:
        user_id = int(args[2])
    except ValueError:
        raise ValueError("ID пользователя должен быть числом")

    return ParsedUserCommand(command=cmd, user_id=user_id)


def execute(conn: sqlite3.Connection, user_input: str) -> str:
    parsed = _parse_user_command(user_input)

    if parsed.command == "add":
        repository.create_user(conn, parsed.user_id)
        return f"Пользователь {parsed.user_id} добавлен"

    if parsed.command == "rm":
        repository.remove_user(conn, parsed.user_id)
        return f"Пользователь {parsed.user_id} удален"

    if parsed.command == "ls":
        users = repository.get_all_users(conn)
        if not users:
            return "Пользователи не найдены"
        return "Список id:\n" + "\n".join([f"`{uid}`" for uid in users])

    raise ValueError(f"Неизвестная команда {parsed.command}")
