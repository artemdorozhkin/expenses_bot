import sqlite3

from expenses_bot.infrastructure import repository

USAGE = (
    "`/user add` id \\- добавить пользователя по id\n"
    "`/user rm` id \\- удалить пользователя по id\n"
    "`/user ls` \\- список id пользователей"
)


def handle(conn: sqlite3.Connection, user_input: str) -> str:
    args = user_input.split(" ")
    if len(args) == 1:
        return USAGE

    try:
        _, cmd, user_id = args
    except ValueError:
        try:
            _, cmd = args
            user_id = -1
        except ValueError:
            return f"Не корректно вызвана команда /user\n\n{USAGE}"
    try:
        user_id = int(user_id)
    except ValueError:
        return f"ID пользователя должен быть числом\n\n{USAGE}"

    try:
        response = _eval_user(conn, cmd, user_id)
    except ValueError as e:
        return f"{e}\n\n{USAGE}"

    return response


def _eval_user(
    conn: sqlite3.Connection,
    cmd: str,
    user_id: int,
) -> str:
    commands = {
        "add": repository.create_user,
        "rm": repository.remove_user,
        "ls": repository.get_all_users,
    }
    if cmd not in commands:
        raise ValueError(f"Неизвестная команда {cmd}")

    command = commands[cmd]
    if cmd == "ls":
        users = command(conn)
        return f"Список id:\n{"\n".join([f'`{uid}`' for uid in users])}"

    command(conn, user_id)
    response = f"Пользователь {user_id} {'удален' if cmd == 'rm' else 'добавлен'}"

    return response
