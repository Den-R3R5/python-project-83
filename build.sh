#!/usr/bin/env bash

uv run tailwindcss -i ./page_analyzer/static/src/input.css -o ./page_analyzer/static/css/style.css --minify

psql -a -d $DATABASE_URL -f database.sql
