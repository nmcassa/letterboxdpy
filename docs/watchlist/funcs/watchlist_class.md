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
  "url": "https://letterboxd.com/nmcassa/watchlist/",
  "count": 82,
  "movies": {
    "1464835": {
      "slug": "the-history-of-concrete",
      "name": "The History of Concrete",
      "year": 2026,
      "url": "https://letterboxd.com/film/the-history-of-concrete/"
    },
    "475935": {
      "slug": "manhunt-2017-1",
      "name": "Manhunt",
      "year": 2017,
      "url": "https://letterboxd.com/film/manhunt-2017-1/"
    },
    "44930": {
      "slug": "the-color-of-money",
      "name": "The Color of Money",
      "year": 1986,
      "url": "https://letterboxd.com/film/the-color-of-money/"
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
