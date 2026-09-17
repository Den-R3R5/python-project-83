from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from validators import url


def _truncate(text):
    if len(text) > 200:
        return text[:200] + "..."
    return text


def link_normalize(link):
    parsed_link = urlparse(link)
    normalized = f"{parsed_link.scheme}://{parsed_link.netloc}".lower()
    return normalized


def link_validate(link):
    if not url(link) and len(link) <= 255:
        return False
    parsed = urlparse(link)
    if parsed.scheme not in ["http", "https"]:
        return False
    return True


def link_response(link):
    response = requests.get(link, timeout=10)
    response.raise_for_status()
    return {
        "response_text": response.text,
        "response_status": response.status_code,
    }


def link_get_tags(response):
    soup = BeautifulSoup(response["response_text"], "html.parser")
    status_code = response["response_status"]
    h1_tag = soup.find("h1")
    title_tag = soup.find("title")
    meta_tag = soup.find("meta", attrs={"name": "description"})

    h1 = ""
    if h1_tag:
        h1 = h1_tag.get_text().strip()

    title = ""
    if title_tag:
        title = title_tag.get_text().strip()

    description = ""
    if meta_tag:
        description = meta_tag.get("content", "").strip()

    return {
        "status_code": status_code,
        "h1": _truncate(h1),
        "title": _truncate(title),
        "description": _truncate(description),
    }
