import re
from letterboxdpy.core.scraper import parse_url
from letterboxdpy.constants.project import DOMAIN


class UserList:
    LIST_PATTERN = f'{DOMAIN}/%s/list/%s'
    LIST_ITEMS_PER_PAGE = 12*5

    def __init__(self, username: str, slug: str) -> None:
        assert re.match("^[A-Za-z0-9_]*$", username), "Invalid author"

        self.username = username
        self.slug = slug
        self.url = self.LIST_PATTERN % (username, slug) 
        self.dom = parse_url(self.url)

    def __str__(self) -> str:
        return f"Not printable object of type: {self.__class__.__name__}"

    def get_title(self) -> str: return extract_title(self.dom)
    def get_author(self) -> str: return extract_author(self.dom)
    def get_description(self) -> str: return extract_description(self.dom)
    def get_date_created(self) -> list: return extract_date_created(self.dom)
    def get_date_updated(self) -> list: return extract_date_updated(self.dom)
    def get_tags(self) -> list: return extract_tags(self.dom)
    def get_movies(self) -> dict: return extract_movies(self.url, self.LIST_ITEMS_PER_PAGE)

def extract_movies(list_url: str, items_per_page) -> dict:
    data = {}

    page = 1
    while True:
        dom = parse_url(f'{list_url}/page/{page}/')
        movies = extract_movies_from_vertical_list(dom)
        data |= movies

        if len(movies) < items_per_page:
            break

        page += 1

    return data

def extract_movies_from_vertical_list(dom, max=20*5) -> dict:
    """
    supports all vertical lists
    ... users' watchlists, users' lists, ...
    """
    items = dom.find_all("div", {"class": "film-poster"})

    movies = {}
    for item in items:
        movie_id = item['data-film-id']
        movie_slug = item['data-film-slug'] 
        movie_name = item.img['alt']

        movies[movie_id] = {
            "slug": movie_slug,
            "name": movie_name,
            'url': f'https://letterboxd.com/film/{movie_slug}/'
        }

    return movies

def extract_title(dom) -> str:
    data = dom.find("meta", attrs={'property': 'og:title'})
    data = data['content'] if 'content' in data.attrs else None
    return data

def extract_author(dom) -> str:
    data = dom.find("span", attrs={'itemprop': 'name'})
    data = data.text if data else None
    return data

def extract_description(dom) -> str:
    data = dom.find("meta", attrs={'property': 'og:description'})
    data = data['content'] if data else None
    return data

def extract_date_created(dom) -> list:
    """
    Scrapes the list page to find and return the creation
    .. date as a string, defaulting to the last updated
    .. date if creation is not available.
    The decorator ensures a valid List is passed.
    """
    data = dom.find("span", {"class": "published is-updated"})

    if data:
        data = data.findChild("time").text
    else:
        data = dom.find("span", {"class": "published"})
        if data: # Watchlists won't have a date created
            data = data.text

    return data

def extract_date_updated(dom) -> list:
    """
    Scrapes the list page to find and return either
    .. the last updated or published date as a string.
    The decorator ensures a valid List is passed.
    """
    data = dom.find("span", {"class": "updated"})

    if data:
        data = data.findChild("time").text
    else:
        data = dom.find("span", {"class": "published"})
        if data: # Watchlists won't have a date updated
            data = data.text

    return data

def extract_tags(dom) -> list:
    """
    Scraping the tag links from a Letterboxd list page and
    .. extracting just the tag names into a clean list.
    The decorator ensures a valid List instance is passed.
    """
    dom = dom.find("ul", {"class": ["tags"]})

    data = []

    if dom:
        dom = dom.findChildren("a")
        for item in dom:
            data.append(item.text)

    return data

