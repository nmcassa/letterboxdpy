<h2 id="print_movies">print_movies(movies: dict, title: str | None = None, max_count: int | None = None)</h2>

Utility helper to print a formatted list of movies to stdout.

```python
from letterboxdpy.films import get_movies_by_year, print_movies

movies = get_movies_by_year(2024, max=10)
print_movies(movies, title="Top Movies of 2024", max_count=5)
```

**Parameters:**
- `movies` (dict): Dictionary of movies keyed by movie ID.
- `title` (str, optional): Header title printed above the list.
- `max_count` (int, optional): Cap the number of printed rows.
