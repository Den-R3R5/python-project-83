import os

import psycopg
from dotenv import load_dotenv
from psycopg.rows import namedtuple_row

load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL")


def _connect():
    return psycopg.connect(DATABASE_URL)


def get_url_by_name(name):
    with _connect() as conn:
        with conn.cursor(row_factory=namedtuple_row) as cur:
            cur.execute(
                "SELECT * FROM urls WHERE name = %s;",
                (name,),
            )
            result = cur.fetchone()
    return result


def get_url_by_id(url_id):
    with _connect() as conn:
        with conn.cursor(row_factory=namedtuple_row) as cur:
            cur.execute(
                "SELECT * FROM urls WHERE id = %s;",
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


def get_all_urls():
    with _connect() as conn:
        with conn.cursor(row_factory=namedtuple_row) as cur:
            cur.execute("SELECT * FROM urls;")
            result = cur.fetchall()
    return result
