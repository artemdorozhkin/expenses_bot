from datetime import datetime
import shutil
import sqlite3
import os
import sys

from expenses_bot.core import config

MIGRATIONS_PATH = "sql/migrations"
ROLLBACKS_PATH = "sql/migrations/rollbacks"


class NotInitError(Exception):
    pass


def init(conn: sqlite3.Connection):
    query = """-- init migrations

CREATE TABLE IF NOT EXISTS schema_migrations (
    filename TEXT PRIMARY KEY,
    applied_at TEXT CURRENT_TIMESTAMP
);
"""
    with open(
        os.path.join(MIGRATIONS_PATH, "001_init.sql"), "w+", encoding="utf-8"
    ) as f:
        f.write(query)
    conn.execute(query)


def get_applied_migrations(conn):
    try:
        return set(
            row[0] for row in conn.execute("SELECT filename FROM schema_migrations")
        )
    except sqlite3.OperationalError as e:
        raise NotInitError(
            "migrations are not initialized. run `migrate.py init` before the first migration"
        ) from e


def apply_migration(conn: sqlite3.Connection, filename: str, is_rollback: bool):
    query_file = os.path.join(
        ROLLBACKS_PATH if is_rollback else MIGRATIONS_PATH, filename
    )
    with open(query_file, "r", encoding="utf-8") as f:
        sql = f.read()
    print(f"Applying {filename}...")
    conn.executescript(sql)
    if is_rollback:
        conn.execute(
            "DELETE FROM schema_migrations WHERE filename = ?",
            (filename.replace("_down", ""),),
        )
    else:
        conn.execute("INSERT INTO schema_migrations (filename) VALUES (?)", (filename,))


def filter_by_args(filenames: list[str], args: list[str]) -> list[str]:
    filtered = []
    for file in filenames:
        for arg in args:
            if file.startswith(arg):
                filtered.append(file)

    return filtered


def make_backup():
    backup_dir = os.path.split(config.DB_FILE)[0]
    backup_file = os.path.join(backup_dir, "backup.db")
    shutil.copyfile(config.DB_FILE, backup_file)


def remove_backup():
    backup_dir = os.path.split(config.DB_FILE)[0]
    backup_file = os.path.join(backup_dir, "backup.db")
    os.remove(backup_file)


def restore_backup():
    backup_dir = os.path.split(config.DB_FILE)[0]
    backup_file = os.path.join(backup_dir, "backup.db")
    shutil.copyfile(backup_file, config.DB_FILE)
    os.remove(backup_file)


def main():
    args = sys.argv
    conn = sqlite3.connect(config.DB_FILE)
    is_rollback = "--down" in args or "-d" in args
    if len(args) == 1:
        filenames = sorted(f for f in os.listdir(MIGRATIONS_PATH) if f.endswith(".sql"))
    else:
        if args[1] == "init":
            init(conn)
            print("Migrations are initialized")
            conn.close()
            return
        if is_rollback:
            filenames = sorted(
                f for f in os.listdir(ROLLBACKS_PATH) if f.endswith(".sql")
            )
            filenames = filter_by_args(filenames, args[1:])
        else:
            filenames = sorted(
                f for f in os.listdir(MIGRATIONS_PATH) if f.endswith(".sql")
            )
            filenames = filter_by_args(filenames, args[1:])

    try:
        applied = get_applied_migrations(conn)
    except NotInitError as e:
        print(f"MIGRATIONS ERR: {e}")
        conn.close()
        return

    make_backup()
    try:
        for file in filenames:
            if file not in applied:
                apply_migration(conn, file, is_rollback)
            else:
                print(f"MIGRATIONS WARN: {file} migration has already been applied")
    except sqlite3.Error as e:
        conn.close()
        restore_backup()
        print(f"MIGRATIONS ERR: {e}")
        return

    remove_backup()
    print("All migrations applied.")
    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()
