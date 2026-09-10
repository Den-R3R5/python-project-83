import os

from dotenv import load_dotenv
from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

from .db import (
    add_check,
    add_url,
    get_all_checks,
    get_all_urls,
    get_url_by_id,
    get_url_by_name,
)
from .utils import link_normalize, link_status, link_validate

load_dotenv()
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/urls")
def urls_post():
    url = request.form.get("url")
    if not link_validate(url):
        flash("Некорректный URL", "failed")
        return render_template("index.html")
    url_normalized = link_normalize(url)
    if get_url_by_name(url_normalized):
        url_id = get_url_by_name(url_normalized).id
        flash("Страница уже существует", "success")
        return redirect(url_for("urls_id_show", url_id=url_id))
    else:
        url_id = add_url(url_normalized)
        flash("Страница успешно добавлена", "success")
        return redirect(url_for("urls_id_show", url_id=url_id))


@app.get("/urls")
def urls_show():
    urls = get_all_urls()
    return render_template("urls/list.html", urls=urls)


@app.get("/urls/<int:url_id>")
def urls_id_show(url_id):
    url_info = get_url_by_id(url_id)
    url_checks = get_all_checks(url_id)
    return render_template("urls/id.html", url=url_info, url_checks=url_checks)


@app.post("/urls/<int:url_id>/checks")
def urls_id_post(url_id):
    url_info = get_url_by_id(url_id)
    try:
        url_status = link_status(url_info.name)
        add_check(url_id, url_status)
        flash("Страница успешно проверена", "success")
    except Exception:
        flash("Произошла ошибка при проверке", "error")
    return redirect(url_for("urls_id_show", url_id=url_id))
