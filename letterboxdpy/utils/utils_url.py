import re
from letterboxdpy.constants.project import DOMAIN_SHORT, URL_PROTOCOLS, DOMAIN


def get_list_slug(url) -> str:
    """
    extract the slug from a URL containing '/list/'.
    example: 'https://letterboxd.com/fastfingertips/list/list_name/' -> 'list_name'
    """
    return url[url.index('/list/') + len('/list/'):].replace('/', '')

def check_url_match(base_url, target_url) -> bool:
    """
    this function checks if two URLs match,
    and returns a boolean value as the result.
    """
    return base_url == target_url or f'{base_url}/' == target_url

def is_short_url(url) -> bool:
    """
    this function checks if the URL is a short URL or not,
    and returns a boolean value as the result.
    """
    return any(prot+DOMAIN_SHORT in url for prot in URL_PROTOCOLS)

def parse_list_url(url: str) -> tuple:
    """Parse list URL to extract username and slug."""
    # URL format: https://letterboxd.com/username/list/slug/
    pattern = r'letterboxd\.com/([^/]+)/list/([^/]+)'
    match = re.search(pattern, url)
    if match:
        return match.group(1), match.group(2)
    raise ValueError(f"Invalid list URL format: {url}")


def build_list_url(username: str, slug: str) -> str:
    """Build list URL from username and slug."""
    return f"{DOMAIN}/{username}/list/{slug}/"