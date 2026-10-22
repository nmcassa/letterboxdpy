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

> [!NOTE]
> No live response is shown here. The example slug could not be verified against
> the live site (the request returned 404), so the output format is not documented
> for this function yet. It returns the same structure as the other `get_movies_by_*` functions.
