#!/usr/bin/env bash

uv run tailwindcss -i ./page_analyzer/static/src/input.css -o ./page_analyzer/static/css/style.css --minify

uv run python -c "from page_analyzer.db import init_db; init_db()"
