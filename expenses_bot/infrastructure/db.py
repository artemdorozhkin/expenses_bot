from datetime import date
import sqlite3
from contextlib import contextmanager
from typing import Any, Generator


def adapt_date_iso(d: date) -> str:
    return d.isoformat()


def convert_date_iso(b: bytes) -> date:
    return date.fromisoformat(b.decode())


sqlite3.register_adapter(date, adapt_date_iso)
sqlite3.register_converter("DATE", convert_date_iso)


@contextmanager
def session(path: str) -> Generator[sqlite3.Connection, Any, None]:
    conn = sqlite3.connect(
        path,
        check_same_thread=False,
        autocommit=False,
    )
    try:
        yield conn
        conn.commit()
    except:
        conn.rollback()
        raise
    finally:
        conn.close()


def init(conn: sqlite3.Connection):
    with open("sql/db.sql", "r", encoding="utf-8") as sql:
        conn.executescript(sql.read())
