from letterboxdpy.scraper import Scraper
import re

from json import (
  JSONEncoder,
  dumps as json_dumps
)


class List:
    DOMAIN = "https://letterboxd.com"

    LIST_CONTAINER = ("ul", {"class": ["poster-list"]})
    WATCHLIST_CONTAINER = ("ul", {"class": ["poster-list"]})

    LIST_PATTERN = f'{DOMAIN}/%s/list/%s'
    WATCHLIST_PATTERN = f'{DOMAIN}/%s/watchlist'

    LIST_ITEMS_PER_PAGE = 12*5
    WATCHLIST_ITEMS_PER_PAGE = 7*4

    def __init__(self, username: str, slug: str=None) -> None:
        assert re.match("^[A-Za-z0-9_]*$", username), "Invalid author"

        # Determine the URL and container based on if a slug was passed
        if slug:
            # If a slug was passed, use the list URL and container
            url = self.LIST_PATTERN % (username, slug) 
            container = self.LIST_CONTAINER
            list_type = "list"
            items_per_page = self.LIST_ITEMS_PER_PAGE
        else:
            # Otherwise use the watchlist URL and container  
            url = self.WATCHLIST_PATTERN % (username)
            container = self.WATCHLIST_CONTAINER
            list_type = "watchlist"
            items_per_page = self.WATCHLIST_ITEMS_PER_PAGE

        # Initialize and get the parsed DOM from the URL
        self.scraper = Scraper(self.DOMAIN)
        dom = self.scraper.get_parsed_page(url) 

        # Set the instance attributes
        self.url = url
        self.slug = slug
        self.username = username
        self.list_type = list_type
        self.items_per_page = items_per_page
        self.title = self.get_title(dom) 
        self.description = self.get_description(dom)
        self.movies = self.get_movies(url, container)
        self.count = len(self.movies)

    def __str__(self):
        return self.jsonify()

    def jsonify(self) -> str:
        return json_dumps(self, indent=4,cls=Encoder)

    def get_title(self, dom) -> str:
        data = dom.find("meta", attrs={'property': 'og:title'})
        data = data['content'] if 'content' in data.attrs else None
        return data

    def get_author(self, dom) -> str:
        data = dom.find("span", attrs={'itemprop': 'name'})
        data = data.text if data else None
        return data

    def get_description(self, dom) -> str:
        data = dom.find("meta", attrs={'property': 'og:description'})
        data = data['content'] if data else None
        return data

    def get_movies(self, url: str, container: tuple) -> list:
        movie_list = []

        page = 1
        while True:
            dom = self.scraper.get_parsed_page(f'{url}/page/{page}/')
            posters = dom.find(*container)
            posters = posters.find_all("img", {"class": ["image"]}) if posters else []

            for poster in posters:
                movie_url = poster.parent['data-film-slug']
                movie_list.append((poster['alt'], movie_url))

            if len(posters) < self.items_per_page:
                break

            page += 1

        return movie_list

class Encoder(JSONEncoder):
    """
    Encoder class provides a way to serialize custom class
    .. instances to JSON by overriding the default serialization
    .. logic to return the object's namespace dictionary.
    """
    def default(self, o):
        return o.__dict__

# -- DECORATORS --

def assert_list_instance(func):
    def wrapper(arg):
        assert isinstance(arg, List), f"function parameter must be a {List.__name__} instance"
        #:optional
        # if not arg.slug:
        #    print(f"WARNING: {func.__name__} function is for regular lists not watchlists.")
        return func(arg)
    return wrapper

# -- FUNCTIONS --

@assert_list_instance
def date_created(instance: List) -> list:
    """
    Scrapes the list page to find and return the creation
    .. date as a string, defaulting to the last updated
    .. date if creation is not available.
    The decorator ensures a valid List is passed.
    """
    dom = instance.scraper.get_parsed_page(instance.url)
    data = dom.find("span", {"class": "published is-updated"})

    if data:
        data = data.findChild("time").text
    else:
        data = dom.find("span", {"class": "published"})
        if data: # Watchlists won't have a date created
            data = data.text

    return data

@assert_list_instance
def date_updated(instance: List) -> list:
    """
    Scrapes the list page to find and return either
    .. the last updated or published date as a string.
    The decorator ensures a valid List is passed.
    """
    dom = instance.scraper.get_parsed_page(instance.url)
    data = dom.find("span", {"class": "updated"})

    if data:
        data = data.findChild("time").text
    else:
        data = dom.find("span", {"class": "published"})
        if data: # Watchlists won't have a date updated
            data = data.text

    return data

@assert_list_instance
def list_tags(instance: List) -> list:
    """
    Scraping the tag links from a Letterboxd list page and
    .. extracting just the tag names into a clean list.
    The decorator ensures a valid List instance is passed.
    """
    dom = instance.scraper.get_parsed_page(instance.url)
    dom = dom.find("ul", {"class": ["tags"]})

    data = []

    if dom:
        dom = dom.findChildren("a")
        for item in dom:
            data.append(item.text)

    return data

if __name__ == "__main__":

    # user list usage:
    list_instance = List("mrbs", "the-suspense-is-killing-us-siku-main-feed-6")
    # print(list_instance) # all attributes
    print('type:', list_instance.list_type)
    print('url:', list_instance.url)
    print('count:', list_instance.count)
    print('created:', date_created(list_instance))
    print('updated:', date_updated(list_instance))
    print('tags:', list_tags(list_instance), end="\n\n")

    # user watchlist usage:
    watchlist_instance = List("mrbs")
    # print(watchlist_instance) # all attributes
    print('type:', watchlist_instance.list_type)
    print('url:', watchlist_instance.url)
    print('count:', watchlist_instance.count)
    print('created:', date_created(watchlist_instance))
    print('updated:', date_updated(watchlist_instance))
    print('tags:', list_tags(watchlist_instance))