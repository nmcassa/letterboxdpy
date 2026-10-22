<h2 id="get_movies_by_genre">get_movies_by_genre(genre: str, max: int | None = None) -> dict</h2>

Fetches popular films within a specific genre.

```python
from letterboxdpy.films import get_movies_by_genre

# Fetch popular sci-fi films
movies = get_movies_by_genre("science-fiction", max=15)

for movie_id, film in movies.items():
    print(f"- {film['name']} ({film.get('rating')})")
```

**Parameters:**
- `genre` (str): Genre slug. Supported genres include:
  `action`, `adventure`, `animation`, `comedy`, `crime`, `documentary`, `drama`, `family`, `fantasy`, `history`, `horror`, `music`, `mystery`, `romance`, `science-fiction`, `thriller`, `tv-movie`, `war`, `western`.
- `max` (int, optional): Maximum number of films to return.

**Returns:**
- `dict`: Dictionary mapping film IDs to movie metadata.

<details>
  <summary>Click to expand demo response</summary>

```json
{
  "47447": {
    "slug": "inception",
    "name": "Inception",
    "year": 2010,
    "rating": 4.19,
    "url": "https://letterboxd.com/film/inception/"
  },
  "117623": {
    "slug": "interstellar",
    "name": "Interstellar",
    "year": 2014,
    "rating": 4.35,
    "url": "https://letterboxd.com/film/interstellar/"
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
