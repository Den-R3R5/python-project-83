PORT ?= 8000

install:
	uv sync 

start:
	uv run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

dev:
dev-flask:
	uv run flask --debug --app page_analyzer:app run

test:
	uv run pytest

test-cov:
	uv run pytest --cov=page_analyzer --cov-report xml

lint:
	uv run ruff check --fix
	uv run ruff format
