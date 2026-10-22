<h2 id="get_movies_by_theme">get_movies_by_theme(theme: str, max: int | None = None) -> dict</h2>

Fetches films matching a Letterboxd theme slug.

```python
from letterboxdpy.films import get_movies_by_theme

# Fetch films matching a theme
movies = get_movies_by_theme("epic-heroes", max=10)

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
  "872871": {
    "slug": "spider-man-brand-new-day",
    "name": "Spider-Man: Brand New Day",
    "year": 2026,
    "url": "https://letterboxd.com/film/spider-man-brand-new-day/",
    "rating": 4.03
  },
  "371378": {
    "slug": "dune-2021",
    "name": "Dune",
    "year": 2021,
    "url": "https://letterboxd.com/film/dune-2021/",
    "rating": 3.89
  },
  "51896": {
    "slug": "the-dark-knight",
    "name": "The Dark Knight",
    "year": 2008,
    "url": "https://letterboxd.com/film/the-dark-knight/",
    "rating": 4.5
  }
}
```
</details>
