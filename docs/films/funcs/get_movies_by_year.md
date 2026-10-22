<h2 id="get_movies_by_year">get_movies_by_year(year: int, max: int | None = None) -> dict</h2>

Fetches popular films released in a specific calendar year.

```python
from letterboxdpy.films import get_movies_by_year

# Fetch popular films from 2024
movies = get_movies_by_year(2024, max=10)

for movie_id, film in movies.items():
    print(f"- {film['name']} ({film.get('rating')})")
```

**Parameters:**
- `year` (int): 4-digit calendar year (e.g. 1999, 2024).
- `max` (int, optional): Maximum number of films to return.

**Returns:**
- `dict`: Dictionary mapping film IDs to movie metadata.
