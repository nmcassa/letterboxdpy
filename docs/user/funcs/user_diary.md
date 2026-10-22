<h2 id="user_diary">get_diary(year=None, month=None, day=None, page=None, fetch_runtime=False, max_workers=None) -> dict</h2>

Fetches a user's diary entries with optional timeframe filters and multithreaded runtime extraction.

```python
from letterboxdpy.user import User

user_instance = User("nmcassa")

# Fetch all diary entries
diary = user_instance.get_diary()
print(diary)

# Or fetch with missing runtime resolution via a thread pool
diary_with_runtimes = user_instance.get_diary(fetch_runtime=True, max_workers=4)

# Timeframe-specific helpers
diary_2024 = user_instance.get_diary_year(2024)
diary_jan = user_instance.get_diary_month(2024, 1)
diary_day = user_instance.get_diary_day(2024, 1, 15)
wrapped = user_instance.get_wrapped(2024)
```

**Parameters:**
- `year` (int, optional): Filter entries by release year.
- `month` (int, optional): Filter entries by month (1-12).
- `day` (int, optional): Filter entries by day (1-31).
- `page` (int, optional): Specific page number to scrape.
- `fetch_runtime` (bool, optional): If `True`, resolves missing movie runtimes using worker threads. Defaults to `False`.
- `max_workers` (int, optional): Maximum worker threads for runtime fetching.

<details>
    <summary>Click to expand demo response</summary>

```json
{
    "entries": {
        "513520182": {
            "name": "Black Swan",
            "slug": "black-swan",
            "id": "20956",
            "release": 2010,
            "runtime": 108,
            "rewatched": false,
            "rating": 4.5,
            "liked": true,
            "reviewed": false,
            "date": {
                "year": 2024,
                "month": 1,
                "day": 15
            },
            "page": 1
        },
        "129707465": {
            "name": "mid90s",
            "slug": "mid90s",
            "id": "370451",
            "release": 2018,
            "runtime": 86,
            "rewatched": false,
            "rating": 4.0,
            "liked": false,
            "reviewed": false,
            "date": {
                "year": 2020,
                "month": 10,
                "day": 20
            },
            "page": 7
        }
    },
    "count": 337,
    "last_page": 7
}
```
</details>