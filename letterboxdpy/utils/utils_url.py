import re
from fastfingertips.url_utils import extract_path_segment
from letterboxdpy.constants.project import DOMAIN_SHORT, URL_PROTOCOLS


def extract_boxd_it_id(url: str) -> str | None:
    """
    extract the boxd.it id from a short url.
    example: 'https://boxd.it/7v7X' -> '7v7X'
    """
    return extract_path_segment(url, after=f"{DOMAIN_SHORT}/")

def get_list_slug(url: str) -> str | None:
    """
    extract the slug from a url containing '/list/'.
    example: 'https://letterboxd.com/fastfingertips/list/list_name/' -> 'list_name'
    """
    return extract_path_segment(url, after='/list/')

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

def get_page_url(base_url: str, page: int, params: str = "") -> str:
    """
    Generate a paginated URL from a base URL and page number.
    Ensures no double slashes and consistent trailing slashes.
    """
    # Remove any trailing slashes from the base URL
    clean_base = base_url.rstrip('/')
    # Letterboxd standard pagination format: /page/N/
    url = f"{clean_base}/page/{page}/"
    if params:
        # Append params, ensuring no double '?'
        url += f"?{params.lstrip('?')}"
    return url
