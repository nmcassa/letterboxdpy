<h2 id="get_watchlist">get_watchlist(filters: dict | None = None) -> dict</h2>

Fetches a user's watchlist with optional filtering capabilities (genres, services, ratings, decades).

```python
from letterboxdpy.user import User

user_instance = User("nmcassa")

# Fetch full watchlist
watchlist = user_instance.get_watchlist()
print(f"Watchlist total count: {user_instance.get_watchlist_count()}")

# Fetch with genre filters (e.g., action but not drama)
filtered = user_instance.get_watchlist({'genre': ['action', '-drama']})
print(f"Matched films: {filtered['data_count']}")
```

You can also use the standalone `Watchlist` class directly:

```python
from letterboxdpy.watchlist import Watchlist

watchlist = Watchlist("nmcassa")
print(f"Total: {watchlist.count}")
print(watchlist.movies)
```

<details>
  <summary>Click to expand demo response</summary>

```json
{
  "available": true,
  "count": 57,
  "data_count": 6,
  "last_page": 1,
  "filters": {
    "genre": [
      "action",
      "-drama"
    ]
  },
  "data": {
    "51397": {
      "name": "From Dusk Till Dawn",
      "slug": "from-dusk-till-dawn",
      "no": 6,
      "page": 1,
      "url": "https://letterboxd.com/films/from-dusk-till-dawn/"
    },
    "62780": {
      "name": "Mad Max: Fury Road",
      "slug": "mad-max-fury-road",
      "no": 1,
      "page": 1,
      "url": "https://letterboxd.com/films/mad-max-fury-road/"
    }
  }
}
```
</details>