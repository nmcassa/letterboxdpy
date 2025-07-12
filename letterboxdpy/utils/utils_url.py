import validators
from letterboxdpy.constants.project import DOMAIN_SHORT, URL_PROTOCOLS


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

def is_url(url) -> bool:
    """
    this function checks if the URL is valid or not,
    and returns a boolean value as the result.
    """
    return validators.url(url)