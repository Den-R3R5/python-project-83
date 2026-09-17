import sys

from requests.exceptions import RequestException

from page_analyzer.db import add_url
from page_analyzer.utils import link_normalize, link_validate


def test_index_get(client):
    assert client.get("/").status_code == 200


def test_link_validate(bad_links_cases):
    for case in bad_links_cases["valid"]:
        assert link_validate(case)
    for case in bad_links_cases["invalid"]:
        assert not link_validate(case)


def test_link_normalize(non_normalized_links_cases):
    for case in non_normalized_links_cases["valid"]:
        assert link_normalize(case) == case
    for case in non_normalized_links_cases["invalid"]:
        assert link_normalize(case) != case
    cases = non_normalized_links_cases["invalid"]
    assert link_normalize(cases[0]) == "https://google.com"
    assert link_normalize(cases[1]) == "http://yandex.ru"
    assert link_normalize(cases[2]) == "https://hexlet.io"


def test_urls_post(client):
    data_1 = {"url": "https://google.com"}
    data_2 = {"url": "google.com"}

    response_valid = client.post("/urls", data=data_1, follow_redirects=True)
    assert response_valid.status_code == 200
    assert "Страница успешно добавлена" in response_valid.text

    response_repeat = client.post("/urls", data=data_1, follow_redirects=True)
    assert response_repeat.status_code == 200
    assert "Страница уже существует" in response_repeat.text

    response_invalid = client.post("/urls", data=data_2)
    assert response_invalid.status_code == 422
    assert "Некорректный URL" in response_invalid.text


def test_urls_show(client):
    assert client.get("/urls").status_code == 200


def test_urls_id_post(client, monkeypatch, html):
    data = {
        "response_text": html,
        "response_status": 200,
    }

    def success(*args, **kwargs):
        return data

    monkeypatch.setattr(
        sys.modules["page_analyzer.app"], "link_response", success
    )

    url_id = add_url("https://site.com")
    response = client.post(f"/urls/{url_id}/checks", follow_redirects=True)

    assert response.status_code == 200
    assert "Страница успешно проверена" in response.text


def test_error_urls_id_post(client, monkeypatch):
    def error(*args, **kwargs):
        raise RequestException("Connection error")

    monkeypatch.setattr(
        sys.modules["page_analyzer.app"],
        "link_response",
        error,
    )
    url_id = add_url("https://broken-site.com")
    response = client.post(f"/urls/{url_id}/checks", follow_redirects=True)

    assert response.status_code == 200
    assert "Произошла ошибка при проверке" in response.text


def test_url_detail_page(client):

    url_id = add_url("https://sitesite.com")

    response = client.get(f"/urls/{url_id}")

    assert response.status_code == 200
    assert "https://sitesite.com" in response.text
