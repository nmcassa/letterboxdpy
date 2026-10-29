# Watchlist Guide

The `Watchlist` class provides tools to inspect and extract a user's saved watchlist, with support for advanced Letterboxd filters.

---

## Quick Example

```python
from letterboxdpy.watchlist import Watchlist

watchlist = Watchlist("nmcassa")
watchlist.movies # lazy load

print(f"Total Watchlist Films: {watchlist.count}")
for movie_id, film in list(watchlist.movies.items())[:5]:
    print(f"- {film['name']} ({film['year']})")
```

??? example "Example `Watchlist` Payload Structure"

    ```json
    {
      "username": "nmcassa",
      "url": "https://letterboxd.com/nmcassa/watchlist",
      "count": 134,
      "movies": {
        "51315": {
          "slug": "videodrome",
          "name": "Videodrome",
          "year": 1983,
          "url": "https://letterboxd.com/film/videodrome/"
        }
      }
    }
    ```

---

## Filtering Watchlists

Letterboxd supports rich URL-based filters on watchlists. You can pass filter dictionaries directly when using the user page handler:

=== "Filter by Genre"
    ```python
    # Positive genre filter
    mystery_watchlist = user.pages.watchlist.get_watchlist(
        filters={"genre": ["mystery"]}
    )

    # Negative genre filter (exclude action)
    no_action = user.pages.watchlist.get_watchlist(
        filters={"genre": ["-action"]}
    )
    ```

=== "Filter by Decade / Year"
    ```python
    # 1990s films in watchlist
    nineties = user.pages.watchlist.get_watchlist(
        filters={"decade": "1990s"}
    )

    # Released in 2023
    released_2023 = user.pages.watchlist.get_watchlist(
        filters={"year": "2023"}
    )
    ```

=== "Filter by Streaming Service"
    ```python
    # Available on Criterion Channel or Netflix
    streaming = user.pages.watchlist.get_watchlist(
        filters={"service": ["criterion-channel"]}
    )
    ```

---

## API Reference

For detailed function definitions, see the [Watchlist API Reference](../api/watchlist.md).
