if __loader__.name == '__main__':
    import sys
    sys.path.append(sys.path[0] + '/..')

import re
from json import (
    dumps as json_dumps,
    loads as json_loads
)

from letterboxdpy.core.encoder import SecretsEncoder
from letterboxdpy.pages import user_watchlist


class Watchlist:

    class WatchlistPages:

        def __init__(self, username: str) -> None:
            self.watchlist = user_watchlist.UserWatchlist(username)

    def __init__(self, username: str) -> None:
        assert re.match("^[A-Za-z0-9_]*$", username), "Invalid author"

        self.username = username
        self.pages = self.WatchlistPages(self.username)

        self.url = self.get_url()
        self.count = self.get_count()

    def __len__(self) -> int:
        return self.count

    def __str__(self) -> str:
        return json_dumps(self, indent=2, cls=SecretsEncoder, secrets=['pages'])

    def jsonify(self) -> dict:
        return json_loads(self.__str__())
    
    def get_owner(self): ...
    def get_url(self) -> str: return self.pages.watchlist.url
    def get_count(self) -> int:  return self.pages.watchlist.get_count()
    def get_movies(self) -> dict:  return self.pages.watchlist.get_movies()


if __name__ == "__main__":
    # user watchlist usage:
    watchlist_instance = Watchlist("nmcassa")
    print(watchlist_instance)
    print('url:', watchlist_instance.url)
    print('count:', watchlist_instance.count)
    print('movies:', watchlist_instance.get_movies())