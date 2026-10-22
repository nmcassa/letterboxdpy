<h2 id="get_movies_by_nanogenre">get_movies_by_nanogenre(nanogenre: str, max: int | None = None) -> dict</h2>

Fetches films matching a specific nanogenre slug.

```python
from letterboxdpy.films import get_movies_by_nanogenre

# Fetch films matching a nanogenre
movies = get_movies_by_nanogenre("post-apocalyptic", max=10)

for movie_id, film in movies.items():
    print(f"- {film['name']} ({film.get('rating')})")
```

**Parameters:**
- `nanogenre` (str): Nanogenre slug.
- `max` (int, optional): Maximum number of films to return.

**Returns:**
- `dict`: Dictionary mapping film IDs to movie metadata.
