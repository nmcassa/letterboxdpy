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
