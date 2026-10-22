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

<details>
  <summary>Click to expand demo response</summary>

```json
{
  "838140": {
    "slug": "the-substance",
    "name": "The Substance",
    "year": 2024,
    "url": "https://letterboxd.com/film/the-substance/",
    "rating": 3.72
  },
  "359505": {
    "slug": "nosferatu-2024",
    "name": "Nosferatu",
    "year": 2024,
    "url": "https://letterboxd.com/film/nosferatu-2024/",
    "rating": 3.65
  },
  "617443": {
    "slug": "dune-part-two",
    "name": "Dune: Part Two",
    "year": 2024,
    "url": "https://letterboxd.com/film/dune-part-two/",
    "rating": 4.37
  }
}
```
</details>
