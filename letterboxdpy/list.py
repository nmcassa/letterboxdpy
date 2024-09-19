from letterboxdpy.parser import get_movies_from_vertical_list
from letterboxdpy.scraper import Scraper
from letterboxdpy.encoder import Encoder
import re

from json import (
  dumps as json_dumps,
  loads as json_loads
)


class List:
    DOMAIN = "https://letterboxd.com"

    LIST_PATTERN = f'{DOMAIN}/%s/list/%s'
    WATCHLIST_PATTERN = f'{DOMAIN}/%s/watchlist'

    LIST_ITEMS_PER_PAGE = 12*5
    WATCHLIST_ITEMS_PER_PAGE = 7*4

    def __init__(self, username: str, slug: str=None) -> None:
        assert re.match("^[A-Za-z0-9_]*$", username), "Invalid author"

        # Determine the URL based on if a slug was passed
        if slug:
            # If a slug was passed, use the list URL
            url = self.LIST_PATTERN % (username, slug) 
            list_type = "list"
            items_per_page = self.LIST_ITEMS_PER_PAGE
        else:
            # Otherwise use the watchlist URL
            url = self.WATCHLIST_PATTERN % (username)
            list_type = "watchlist"
            items_per_page = self.WATCHLIST_ITEMS_PER_PAGE

        # Fetch the parsed DOM from the specified URL.
        dom = Scraper.get_parsed_page(url) 

        # Set the instance attributes
        self.url = url
        self.slug = slug
        self.username = username
        self.list_type = list_type
        self.items_per_page = items_per_page

        # supports: list
        self.title = self.get_title(dom) 
        self.author = self.get_author(dom)
        self.date_created = self.get_date_created(dom)
        self.date_updated = self.get_date_updated(dom)
        self.tags = self.get_tags(dom)

        self.movies = self.get_movies(url)
        self.count = len(self.movies)

    def __str__(self):
      return json_dumps(self, indent=2, cls=Encoder)

    def jsonify(self):
      return json_loads(self.__str__())

    def get_movies(self, url: str) -> dict:
        data = {}

        page = 1
        while True:
            dom = Scraper.get_parsed_page(f'{url}/page/{page}/')
            movies = get_movies_from_vertical_list(dom)
            data |= movies

            if len(movies) < self.items_per_page:
                break

            page += 1

        return data

    @staticmethod
    def get_title(dom) -> str:
        data = dom.find("meta", attrs={'property': 'og:title'})
        data = data['content'] if 'content' in data.attrs else None
        return data

    @staticmethod
    def get_author(dom) -> str:
        data = dom.find("span", attrs={'itemprop': 'name'})
        data = data.text if data else None
        return data

    @staticmethod
    def get_description(dom) -> str:
        data = dom.find("meta", attrs={'property': 'og:description'})
        data = data['content'] if data else None
        return data

    @staticmethod
    def get_date_created(dom) -> list:
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

    @staticmethod
    def get_date_updated(dom) -> list:
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

    @staticmethod
    def get_tags(dom) -> list:
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

if __name__ == "__main__":

    # user list usage:
    list_instance = List("mrbs", "the-suspense-is-killing-us-siku-main-feed-6")
    # print(list_instance) # all attributes
    print('type:', list_instance.list_type)
    print('url:', list_instance.url)
    print('count:', list_instance.count)
    print('created:', list_instance.date_created)
    print('updated:', list_instance.date_updated)
    print('tags:', list_instance.tags, end="\n"*2)

    # user watchlist usage:
    watchlist_instance = List("mrbs")
    # print(watchlist_instance) # all attributes
    print('type:', watchlist_instance.list_type)
    print('url:', watchlist_instance.url)
    print('count:', watchlist_instance.count)
    print('created:', watchlist_instance.date_created)
    print('updated:', watchlist_instance.date_updated)
    print('tags:', watchlist_instance.tags, end="\n"*2)