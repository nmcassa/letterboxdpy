import re
from json import (
    dumps as json_dumps,
    loads as json_loads
)

from letterboxdpy.core.encoder import SecretsEncoder
from letterboxdpy.pages import user_list


class List:

    class ListPages:

        def __init__(self, username: str, slug: str) -> None:
            self.list = user_list.UserList(username, slug)

    def __init__(self, username: str, slug: str=None) -> None:
        assert re.match("^[A-Za-z0-9_]*$", username), "Invalid author"

        self.username = username.lower()
        self.slug = slug
        self.pages = self.ListPages(self.username, self.slug)

        self.url = self.get_url()
        self.title = self.get_title()
        self.author = self.get_author()
        self.description = self.get_description()
        self.date_created = self.get_date_created()
        self.date_updated = self.get_date_updated()
        self.tags = self.get_tags()
        self.count = self.get_count()

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
        return json_dumps(self, indent=2, cls=SecretsEncoder, secrets=['pages'])

    def jsonify(self) -> dict:
        return json_loads(self.__str__())

    def get_url(self) -> str: return self.pages.list.url
    def get_title(self) -> list: return self.pages.list.get_tags()
    def get_author(self) -> str: return self.pages.list.get_author()
    def get_description(self) -> str: return self.pages.list.get_description()
    def get_date_created(self) -> list: return self.pages.list.get_date_created()
    def get_date_updated(self) -> list: return self.pages.list.get_date_updated()
    def get_tags(self) -> list: return self.pages.list.get_tags()
    def get_movies(self) -> dict: return self.pages.list.get_movies()
    def get_count(self) -> int: return self.pages.list.get_count()

if __name__ == "__main__":
    # user list usage:
    list_instance = List("mrbs", "the-suspense-is-killing-us-siku-main-feed-6")
    print(list_instance)
    print('url:', list_instance.url)
    print('title:' , list_instance.title)
    print('authır:', list_instance.author)
    print('description:', list_instance.description)
    print('created:', list_instance.date_created)
    print('updated:', list_instance.date_updated)
    print('tags:', list_instance.tags)
    # print('movies:', list_instance.get_movies())
    print('count:', list_instance.count)