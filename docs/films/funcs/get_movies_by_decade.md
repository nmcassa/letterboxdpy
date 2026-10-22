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
  "49455": {
    "slug": "scream",
    "name": "Scream",
    "year": 1996,
    "url": "https://letterboxd.com/film/scream/",
    "rating": 4.02
  },
  "51782": {
    "slug": "the-silence-of-the-lambs",
    "name": "The Silence of the Lambs",
    "year": 1991,
    "url": "https://letterboxd.com/film/the-silence-of-the-lambs/",
    "rating": 4.34
  },
  "49047": {
    "slug": "10-things-i-hate-about-you",
    "name": "10 Things I Hate About You",
    "year": 1999,
    "url": "https://letterboxd.com/film/10-things-i-hate-about-you/",
    "rating": 4.07
  }
}
```
</details>
