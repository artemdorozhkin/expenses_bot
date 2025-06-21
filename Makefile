.PHONY: run, install, tests

run:
	pipenv run python -m expenses_bot

install:
	pipenv install

tests:
	pipenv run python -m pytest tests