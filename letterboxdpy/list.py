from scraper import Scraper
import re

from json import (
  JSONEncoder,
  dumps as json_dumps
)


class List:
    DOMAIN = "https://letterboxd.com"

    def __init__(self, author: str, title: str) -> None:
        assert re.match("^[A-Za-z0-9_]*$", author), "Invalid author"
        assert isinstance(title, str), "title must be a string"

        self.scraper = Scraper(self.DOMAIN)
        self.title = title.replace(' ', '-').lower()
        self.author = author.lower()

        if title != '/watchlist/': # For regular lists
            self.url = f'https://letterboxd.com/{self.author}/list/{self.title}/'
        else: # For watchlists
            self.url = f'https://letterboxd.com/{self.author}/watchlist/'

        dom = self.scraper.get_parsed_page(self.url)
        self.description = self.get_description(dom)
        self.film_count(self.url)

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

    #:edit-syntax
    def film_count(self, url: str) -> int: #and movie_list!!
        prev = count = 0
        curr = 1
        movie_list = []
        while prev != curr:
            count += 1
            prev = len(movie_list)
            page = self.scraper.get_parsed_page(url + "page/" + str(count) + "/")

            if self.url.find('/list/') != -1: # For regular lists
                img = page.find("ul",{"class": ["js-list-entries poster-list -p125 -grid film-list"], })
            else: # For watchlists
                img = page.find("ul",{"class": ["poster-list -p125 -grid -scaled128"], })
            if img:
                img = img.find_all("img", {"class": ["image"], })

                for item in img:
                    movie_url = item.parent['data-film-slug']
                    movie_list.append((item['alt'], movie_url))
                
            curr = len(movie_list)

        self.filmCount = curr
        self.movies = movie_list

        if curr == 0 and self.url.find('/list/') != -1: # No exception needed for an empty watchlist
            raise Exception("No list exists")

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
    
    # user watchlist usage:
    watchlist_instance =  List("mrbs", "/watchlist/")
    print(watchlist_instance)
    # print(date_created(watchlist_instance)) # None
    # print(date_updated(watchlist_instance)) # None
    # print(list_tags(watchlist_instance)) # empty list

    # user list usage:
    list_instance = List("mrbs", "the-suspense-is-killing-us-siku-main-feed-6")
    print(list_instance)
    print(date_created(list_instance))
    print(date_updated(list_instance))
    print(list_tags(list_instance))