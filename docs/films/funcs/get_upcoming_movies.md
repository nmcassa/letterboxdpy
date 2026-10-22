<h2 id="get_upcoming_movies">get_upcoming_movies(max: int | None = None) -> dict</h2>

Fetches upcoming popular films from Letterboxd's upcoming section.

```python
from letterboxdpy.films import get_upcoming_movies

# Fetch upcoming films
upcoming = get_upcoming_movies(max=10)

for movie_id, film in upcoming.items():
    print(f"- {film['name']} ({film.get('url')})")
```

**Parameters:**
- `max` (int, optional): Maximum number of films to return.

**Returns:**
- `dict`: Dictionary mapping film IDs to movie metadata.

<details>
  <summary>Click to expand demo response</summary>

```json
{
  "1197499": {
    "slug": "marty-supreme",
    "name": "Marty Supreme",
    "year": 2025,
    "rating": null,
    "url": "https://letterboxd.com/film/marty-supreme/"
  },
  "772232": {
    "slug": "hamnet",
    "name": "Hamnet",
    "year": 2025,
    "rating": null,
    "url": "https://letterboxd.com/film/hamnet/"
  },
  "1116600": {
    "slug": "sinners-2025",
    "name": "Sinners",
    "year": 2025,
    "rating": null,
    "url": "https://letterboxd.com/film/sinners-2025/"
  }
}
```
</details>
