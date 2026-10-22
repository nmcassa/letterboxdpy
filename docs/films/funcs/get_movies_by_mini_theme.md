<h2 id="get_movies_by_mini_theme">get_movies_by_mini_theme(theme: str, max: int | None = None) -> dict</h2>

Fetches films matching a Letterboxd mini-theme slug.

```python
from letterboxdpy.films import get_movies_by_mini_theme

# Fetch films matching a mini-theme
movies = get_movies_by_mini_theme("cyberpunk", max=10)

for movie_id, film in movies.items():
    print(f"- {film['name']} ({film.get('rating')})")
```

**Parameters:**
- `theme` (str): Mini-theme slug.
- `max` (int, optional): Maximum number of films to return.

**Returns:**
- `dict`: Dictionary mapping film IDs to movie metadata.

<details>
  <summary>Click to expand demo response</summary>

```json
{
  "51848": {
    "slug": "blade-runner-2049",
    "name": "Blade Runner 2049",
    "year": 2017,
    "rating": 4.15,
    "url": "https://letterboxd.com/film/blade-runner-2049/"
  },
  "51847": {
    "slug": "blade-runner",
    "name": "Blade Runner",
    "year": 1982,
    "rating": 4.21,
    "url": "https://letterboxd.com/film/blade-runner/"
  },
  "51853": {
    "slug": "akira",
    "name": "Akira",
    "year": 1988,
    "rating": 4.20,
    "url": "https://letterboxd.com/film/akira/"
  }
}
```
</details>
