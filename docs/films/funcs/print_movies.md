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

<details>
  <summary>Click to expand demo output</summary>

```text
Top Movies of 2024 -- (10 movies)
****************************************************************
1        834656   Civil War
2        488751   Monkey Man
3        768407   Dune: Part Two
4        710352   Poor Things
5        703077   Magazine Dreams
****************************************************************
```
</details>
