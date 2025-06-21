import Levenshtein

from expenses_bot.db import CategoryRepository


def validate_category(name: str) -> str | None:
    categories = CategoryRepository().get_all()
    names = [c.name for c in categories]

    for n in names:
        if name.lower() in n.lower():
            return n

    rate = [Levenshtein.ratio(n, name) for n in names]
    max_rate = max(rate)
    return None if max_rate < 0.65 else names[rate.index(max_rate)]
