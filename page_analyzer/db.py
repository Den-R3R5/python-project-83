import os

import psycopg
from dotenv import load_dotenv
from psycopg.rows import namedtuple_row

load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL")


def init_db():
    with _connect() as conn:
        with conn.cursor() as cur:
            with open("database.sql", "r") as f:
                cur.execute(f.read())
            conn.commit()


def _connect():
    return psycopg.connect(DATABASE_URL)


def get_url_by_name(name):
    with _connect() as conn:
        with conn.cursor(row_factory=namedtuple_row) as cur:
            cur.execute(
                """
                SELECT
                    id,
                    name,
                    TO_CHAR(urls.created_at, 'YYYY-MM-DD') as created_at
                FROM urls 
                WHERE name = %s;""",
                (name,),
            )
            result = cur.fetchone()
    return result


def get_url_by_id(url_id):
    with _connect() as conn:
        with conn.cursor(row_factory=namedtuple_row) as cur:
            cur.execute(
                """
                SELECT 
                    id,
                    name,
                    TO_CHAR(urls.created_at, 'YYYY-MM-DD') as created_at
                FROM urls 
                WHERE id = %s;""",
                (url_id,),
            )
            result = cur.fetchone()
    return result


def add_url(name):
    with _connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO urls(name) VALUES(%s) RETURNING id",
                (name,),
            )
            url_id = cur.fetchone()[0]
            conn.commit()
    return url_id


def add_check(url_id, status_code, h1, title, description):
    with _connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO 
                url_checks(url_id, status_code, h1, title, description) 
                VALUES(%s, %s, %s, %s, %s)""",
                (url_id, status_code, h1, title, description),
            )
            conn.commit()


def get_all_checks(url_id):
    with _connect() as conn:
        with conn.cursor(row_factory=namedtuple_row) as cur:
            cur.execute(
                """
                SELECT
                    id,
                    url_id,
                    status_code,
                    h1,
                    title,
                    description,
                    TO_CHAR(url_checks.created_at, 'YYYY-MM-DD') as created_at
                FROM url_checks WHERE url_id = %s 
                ORDER BY id DESC;""",
                (url_id,),
            )
            result = cur.fetchall()
    return result


def get_all_urls():
    with _connect() as conn:
        with conn.cursor(row_factory=namedtuple_row) as cur:
            cur.execute(
                """
                SELECT DISTINCT ON (urls.id)
                    urls.id,
                    urls.name,
                    TO_CHAR(url_checks.created_at, 'YYYY-MM-DD'),
                    url_checks.status_code
                FROM urls
                LEFT JOIN url_checks ON urls.id = url_checks.url_id
                ORDER BY urls.id DESC, url_checks.id DESC;"""
            )
            result = cur.fetchall()
    return result
