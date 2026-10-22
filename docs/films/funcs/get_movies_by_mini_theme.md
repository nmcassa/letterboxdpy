<h2 id="get_movies_by_mini_theme">get_movies_by_mini_theme(theme: str, max: int | None = None) -> dict</h2>

Fetches films matching a Letterboxd mini-theme slug.

```python
from letterboxdpy.films import get_movies_by_mini_theme

# Fetch films matching a mini-theme
movies = get_movies_by_mini_theme("terrorism-thriller-gripping-intense-political", max=10)

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
  "784328": {
    "slug": "oppenheimer-2023",
    "name": "Oppenheimer",
    "year": 2023,
    "url": "https://letterboxd.com/film/oppenheimer-2023/",
    "rating": 4.16
  },
  "951277": {
    "slug": "one-battle-after-another",
    "name": "One Battle After Another",
    "year": 2025,
    "url": "https://letterboxd.com/film/one-battle-after-another/",
    "rating": 4.12
  },
  "877253": {
    "slug": "conclave",
    "name": "Conclave",
    "year": 2024,
    "url": "https://letterboxd.com/film/conclave/",
    "rating": 3.92
  }
}
```
</details>
