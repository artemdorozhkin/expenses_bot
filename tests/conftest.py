import pytest

from expenses_bot import db


@pytest.fixture
def conn():
    with db.session(":memory:") as conn:
        db.init(conn)
        yield conn
