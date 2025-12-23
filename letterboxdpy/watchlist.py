"""
Watchlist module.
Provides the Watchlist class for accessing user watchlist data.
"""
if __loader__.name == '__main__':
    import sys
    sys.path.append(sys.path[0] + '/..')

import re

from letterboxdpy.utils.utils_file import JsonFile
from letterboxdpy.core.encoder import SecretsEncoder
from letterboxdpy.pages import user_watchlist
from letterboxdpy.core.exceptions import PrivateRouteError


class Watchlist:

    class WatchlistPages:

        def __init__(self, username: str) -> None:
            self.watchlist = user_watchlist.UserWatchlist(username)

    def __init__(self, username: str) -> None:
        assert re.match("^[A-Za-z0-9_]+$", username), "Invalid author"

        self.username = username
        self.pages = self.WatchlistPages(self.username)

        self.url = self.get_url()
        self.count = self.get_count()

        self._movies = None

    # Properties
    @property
    def movies(self) -> dict:
        if self._movies is None:
            self._movies = self.get_movies()
        return self._movies

    # Magic Methods
    def __len__(self) -> int:
        return self.count

    def __str__(self) -> str:
        return JsonFile.stringify(self, indent=2, encoder=SecretsEncoder, secrets=['pages'])

    def jsonify(self) -> dict:
        return JsonFile.parse(self.__str__())

    # Data Retrieval Methods
    def get_owner(self) -> str: return self.pages.watchlist.get_owner()
    def get_url(self) -> str: return self.pages.watchlist.url
    def get_count(self) -> int:  return self.pages.watchlist.get_count()
    def get_movies(self) -> dict:  return self.pages.watchlist.get_movies()


if __name__ == "__main__":
    import argparse
    import sys

    sys.stdout.reconfigure(encoding='utf-8')

    parser = argparse.ArgumentParser(description="Fetch a user's watchlist.")
    parser.add_argument('--user', '-u', help="Username to fetch watchlist for", required=False)
    args = parser.parse_args()

    username = args.user or input('Enter username: ').strip()

    while not username:
        username = input('Please enter a valid username: ').strip()

    print(f"Fetching watchlist for username: {username}")

    # Watchlist usage:
    watchlist_instance = Watchlist(username)
    print(watchlist_instance)
    try:
        print('URL:', watchlist_instance.url)
        print('Count:', watchlist_instance.count)
        print('Movies:', watchlist_instance.movies)
    except PrivateRouteError:
        print(f"Error: User's watchlist is private.")
