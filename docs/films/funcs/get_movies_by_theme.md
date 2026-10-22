<h2 id="get_movies_by_theme">get_movies_by_theme(theme: str, max: int | None = None) -> dict</h2>

Fetches films matching a Letterboxd theme slug.

```python
from letterboxdpy.films import get_movies_by_theme

# Fetch films matching a theme
movies = get_movies_by_theme("time-loop", max=10)

for movie_id, film in movies.items():
    print(f"- {film['name']} ({film.get('rating')})")
```

**Parameters:**
- `theme` (str): Theme slug.
- `max` (int, optional): Maximum number of films to return.

**Returns:**
- `dict`: Dictionary mapping film IDs to movie metadata.

<details>
  <summary>Click to expand demo response</summary>

```json
{
  "51855": {
    "slug": "groundhog-day",
    "name": "Groundhog Day",
    "year": 1993,
    "rating": 4.10,
    "url": "https://letterboxd.com/film/groundhog-day/"
  },
  "51856": {
    "slug": "edge-of-tomorrow",
    "name": "Edge of Tomorrow",
    "year": 2014,
    "rating": 3.96,
    "url": "https://letterboxd.com/film/edge-of-tomorrow/"
  },
  "51857": {
    "slug": "palm-springs-2020",
    "name": "Palm Springs",
    "year": 2020,
    "rating": 3.79,
    "url": "https://letterboxd.com/film/palm-springs-2020/"
  }
}
```
</details>
