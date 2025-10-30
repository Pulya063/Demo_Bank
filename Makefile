.PHONY: install test lint format typecheck coverage

install:
	pip install -r requirements-dev.txt

test:
	pytest -q

coverage:
	pytest --cov=app --cov-report=term --cov-report=xml

lint:
	ruff check .

format:
	black .
	isort .

typecheck:
	mypy .