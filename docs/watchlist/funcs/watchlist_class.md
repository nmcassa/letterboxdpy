<h2 id="watchlist_class">Watchlist Class</h2>

Provides access to a user's watchlist with lazy loading and error handling for private accounts.

```python
from letterboxdpy.watchlist import Watchlist
from letterboxdpy.core.exceptions import PrivateRouteError

watchlist = Watchlist("nmcassa")

try:
    print(f"Watchlist Owner: {watchlist.get_owner()}")
    print(f"Film Count: {watchlist.count}")
    print(f"URL: {watchlist.url}")

    # Access movies dictionary (lazy loaded)
    for film_id, film in watchlist.movies.items():
        print(f"- {film['name']} ({film['year']})")
except PrivateRouteError:
    print("User's watchlist is private.")
```

<details>
  <summary>Click to expand demo response</summary>

```json
{
  "username": "nmcassa",
  "url": "https://letterboxd.com/nmcassa/watchlist",
  "count": 76,
  "movies": {
    "51315": {
      "slug": "videodrome",
      "name": "Videodrome",
      "year": 1983,
      "url": "https://letterboxd.com/film/videodrome/"
    },
    "703077": {
      "slug": "magazine-dreams",
      "name": "Magazine Dreams",
      "year": 2023,
      "url": "https://letterboxd.com/film/magazine-dreams/"
    }
  }
}
```
</details>

### Attributes & Methods

- `username` (str): Target username.
- `url` (str): Canonical watchlist URL (`https://letterboxd.com/{username}/watchlist/`).
- `count` (int): Total film count.
- `movies` (dict): Lazy-loaded dictionary of films.
- `get_owner()` (str): Returns the username.
