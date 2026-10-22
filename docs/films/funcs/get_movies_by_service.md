<h2 id="get_movies_by_service">get_movies_by_service(service: str, max: int | None = None) -> dict</h2>

Fetches popular films streaming on a specific streaming service.

```python
from letterboxdpy.films import get_movies_by_service

# Fetch popular films available on Netflix
movies = get_movies_by_service("netflix", max=10)

for movie_id, film in movies.items():
    print(f"- {film['name']} ({film.get('rating')})")
```

**Parameters:**
- `service` (str): Streaming provider slug. Examples include:
  `netflix`, `hulu`, `prime-video`, `disney-plus`, `apple-tv`, `hbo-max`, `peacock`, `mubi`, `criterion-channel`.
- `max` (int, optional): Maximum number of films to return.

**Returns:**
- `dict`: Dictionary mapping film IDs to movie metadata.
