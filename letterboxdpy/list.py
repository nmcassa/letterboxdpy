if __loader__.name == '__main__':
    import sys
    sys.path.append(sys.path[0] + '/..')

import re

from letterboxdpy.utils.utils_file import JsonFile
from letterboxdpy.core.encoder import SecretsEncoder
from letterboxdpy.pages import user_list
from letterboxdpy.pages.user_list import ListMetaData


class List:

    class ListPages:

        def __init__(self, username: str, slug: str) -> None:
            self.list = user_list.UserList(username, slug)

    def __init__(self, username: str, slug: str = None) -> None:
        assert re.match("^[A-Za-z0-9_]+$", username), "Invalid author"

        self.username = username.lower()
        self.slug = slug
        self.pages = self.ListPages(self.username, self.slug)

        self._movies = None

        self.url = self.get_url()
        self.title = self.get_title()
        self.author = self.get_author()
        self.description = self.get_description()
        self.date_created = self.get_date_created()
        self.date_updated = self.get_date_updated()
        self.tags = self.get_tags()
        self.count = self.get_count()
        self.list_id = self.get_list_id()

    # Properties
    @property
    def movies(self) -> dict:
        if self._movies is None:
            self._movies = self.get_movies()
        return self._movies

    # Magic Methods
    def __len__(self) -> int:
        return self.count

    def __getattr__(self, name):
        if not object.__getattribute__(self, name):
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

        method = object.__getattribute__(self, name)
        if callable(method):
            return method
        else:
            raise TypeError(f"'{self.__class__.__name__}' object attribute '{name}' is not callable")

    def __getitem__(self, key: str):
        try:
            return object.__getattribute__(self, key)
        except AttributeError:
            raise KeyError(f"'{self.__class__.__name__}' object has no key '{key}'")

    def __str__(self) -> str:
        return JsonFile.stringify(self, indent=2, encoder=SecretsEncoder, secrets=['pages'])

    def jsonify(self) -> dict:
        return JsonFile.parse(self.__str__())

    # Data Retrieval Methods
    def get_url(self) -> str: return self.pages.list.url
    def get_title(self) -> str: return self.pages.list.get_title()
    def get_author(self) -> str: return self.pages.list.get_author()
    def get_description(self) -> str: return self.pages.list.get_description()
    def get_date_created(self) -> list: return self.pages.list.get_date_created()
    def get_date_updated(self) -> list: return self.pages.list.get_date_updated()
    def get_tags(self) -> list: return self.pages.list.get_tags()
    def get_movies(self) -> dict: return self.pages.list.get_movies()
    def get_count(self) -> int: return self.pages.list.get_count()
    def get_list_id(self) -> str: return self.pages.list.get_list_id()
    def get_list_meta(self, url: str) -> ListMetaData: return self.pages.list.get_list_meta(url)

if __name__ == "__main__":
    # user list usage:
    list_instance = List("nmcassa", "def-con-movie-list")
    movies = list_instance.movies
    assert len(movies) == list_instance.count, "Count mismatch"

    print(list_instance)
    print('url:', list_instance.url)
    print('title:', list_instance.title)
    print('author:', list_instance.author)
    print('description:', list_instance.description)
    print('created:', list_instance.date_created)
    print('updated:', list_instance.date_updated)
    print('tags:', list_instance.tags)
    print('count:', list_instance.count)
    print('list_id:', list_instance.list_id)
    print('movies:', movies)