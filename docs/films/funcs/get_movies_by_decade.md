<h2 id="get_movies_by_decade">get_movies_by_decade(decade: int, max: int | None = None) -> dict</h2>

Fetches popular films for a specific decade from Letterboxd.

```python
from letterboxdpy.films import get_movies_by_decade

# Fetch popular films from the 1990s
movies = get_movies_by_decade(1990, max=10)

for movie_id, film in movies.items():
    print(f"- {film['name']} (Score: {film.get('rating', 'unrated')})")
```

**Parameters:**
- `decade` (int): The starting year of the decade (e.g. 1980, 1990, 2000).
- `max` (int, optional): Maximum number of films to return. Defaults to `None` (all films from first page).

**Returns:**
- `dict`: Dictionary mapping film IDs to movie dictionaries (`slug`, `name`, `rating`, `url`).

<details>
  <summary>Click to expand demo response</summary>

```json
{
  "51846": {
    "slug": "fight-club",
    "name": "Fight Club",
    "year": 1999,
    "rating": 4.28,
    "url": "https://letterboxd.com/film/fight-club/"
  },
  "51842": {
    "slug": "pulp-fiction",
    "name": "Pulp Fiction",
    "year": 1994,
    "rating": 4.45,
    "url": "https://letterboxd.com/film/pulp-fiction/"
  },
  "20593": {
    "slug": "the-matrix",
    "name": "The Matrix",
    "year": 1999,
    "rating": 4.42,
    "url": "https://letterboxd.com/film/the-matrix/"
  }
}
```
</details>
