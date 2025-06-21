from expenses_bot import validators


def test_correct_category():
    user_input = "продукты"

    result = validators.validate_category(user_input)

    assert "Продукты" == result


def test_guess_category():
    user_input = "транспортные"

    result = validators.validate_category(user_input)

    assert "Транспорт" == result


def test_not_guess_category():
    user_input = "Без категории"

    result = validators.validate_category(user_input)

    assert result is None
