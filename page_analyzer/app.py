import os

from dotenv import load_dotenv
from flask import (
    Flask,
    flash,
    get_flashed_messages,
    redirect,
    render_template,
    url_for,
)

load_dotenv()
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")


@app.get("/")
def index():
    messages = get_flashed_messages(with_categories=True)

    return render_template(
        "index.html",
        messages=messages,
    )

