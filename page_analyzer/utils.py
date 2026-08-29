from urllib.parse import urlparse

from validators import url


def link_normalize(link):
    parsed_link = urlparse(link)
    normalized = f"{parsed_link.scheme}://{parsed_link.netloc}".lower()
    return normalized


def link_validate(link):
    if url(link) and len(link) <= 255:
        return True
    return False
