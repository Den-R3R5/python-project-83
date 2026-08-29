from urllib.parse import urlparse


def link_normalize(link):
    parsed_link = urlparse(link)
    normalized = f"{parsed_link.scheme}://{parsed_link.netloc}".lower()
    return normalized
