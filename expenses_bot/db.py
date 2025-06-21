from expenses_bot import fakedb
from expenses_bot.models import Category


class CategoryRepository:
    def get_all(self) -> list[Category]:
        return [Category(name) for name in fakedb.categories]
