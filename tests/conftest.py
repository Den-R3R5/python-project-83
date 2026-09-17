import os

import pytest

from page_analyzer.app import app
from page_analyzer.db import _connect, init_db

os.environ["DATABASE_URL"] = os.getenv(
    "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/postgres"
)


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    with _connect() as conn:
        with conn.cursor() as cur:
            cur.execute("DROP TABLE IF EXISTS url_checks, urls CASCADE;")
        conn.commit()
    init_db()
    try:
        yield
    finally:
        with _connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "TRUNCATE urls, url_checks RESTART IDENTITY CASCADE;"
                )
            conn.commit()


@pytest.fixture()
def client():
    return app.test_client()


@pytest.fixture()
def bad_links_cases():
    return {
        "valid": [
            "https://google.com",
            "http://yandex.ru",
            "https://hexlet.io",
        ],
        "invalid": [
            "google.com",
            "just-text",
            "http://",
            "://google.com",
        ],
    }


@pytest.fixture()
def non_normalized_links_cases():
    return {
        "valid": [
            "https://google.com",
            "http://yandex.ru",
            "https://hexlet.io",
        ],
        "invalid": [
            "https://google.com/%D6%D5",
            "http://yandex.ru/randomstaff",
            "https://hexlet.io/courses/6",
        ],
    }


@pytest.fixture()
def html():
    return """<!doctype html>
<html lang="ru">
  <head>
    <meta charset="UTF-8" />
    <title>
      Тестовый заголовок - Lorem ipsum dolor sit amet, consectetur adipiscing
      elit. Ut iaculis iaculis efficitur. Nullam facilisis, est vel porttitor
      sollicitudin, ligula lectus accumsan neque, ut efficitur metus eros id mi.
      Praesent sit amet risus arcu. Vestibulum quis efficitur enim, at tincidunt
      mauris. Fusce laoreet nisl porttitor lorem tristique blandit. Pellentesque
      habitant morbi tristique senectus et netus et malesuada.
    </title>
    <meta
      name="description"
      content="Описание - Lorem ipsum dolor sit amet, consectetur adipiscing
      elit. Ut iaculis iaculis efficitur. Nullam facilisis, est vel porttitor
      sollicitudin, ligula lectus accumsan neque, ut efficitur metus eros id mi.
      Praesent sit amet risus arcu. Vestibulum quis efficitur enim, at tincidunt
      mauris. Fusce laoreet nisl porttitor lorem tristique blandit. Pellentesque
      habitant morbi tristique senectus et netus et malesuada./>
  </head>
  <body>
    <h1>
      h1 - Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut iaculis
      iaculis efficitur. Nullam facilisis, est vel porttitor sollicitudin,
      ligula lectus accumsan neque, ut efficitur metus eros id mi. Praesent sit
      amet risus arcu. Vestibulum quis efficitur enim, at tincidunt mauris.
      Fusce laoreet nisl porttitor lorem tristique blandit. Pellentesque
      habitant morbi tristique senectus et netus et malesuada.
    </h1>
    <p>
      Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut iaculis
      iaculis efficitur. Nullam facilisis, est vel porttitor sollicitudin,
      ligula lectus accumsan neque, ut efficitur metus eros id mi. Praesent sit
      amet risus arcu. Vestibulum quis efficitur enim, at tincidunt mauris.
      Fusce laoreet nisl porttitor lorem tristique blandit. Pellentesque
      habitant morbi tristique senectus et netus et malesuada.
    </p>
  </body>
</html>
    """
