.PHONY: run, install, tests

run:
	pipenv run python -m expenses_bot

install:
	pipenv install

migrate:
	pipenv run python migrate.py $(M)

tests:
	pipenv run python -m pytest tests