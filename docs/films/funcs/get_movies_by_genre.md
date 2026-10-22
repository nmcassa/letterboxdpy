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
  "117621": {
    "slug": "interstellar",
    "name": "Interstellar",
    "year": 2014,
    "url": "https://letterboxd.com/film/interstellar/",
    "rating": 4.46
  },
  "611288": {
    "slug": "project-hail-mary",
    "name": "Project Hail Mary",
    "year": 2026,
    "url": "https://letterboxd.com/film/project-hail-mary/",
    "rating": 4.31
  },
  "872871": {
    "slug": "spider-man-brand-new-day",
    "name": "Spider-Man: Brand New Day",
    "year": 2026,
    "url": "https://letterboxd.com/film/spider-man-brand-new-day/",
    "rating": 4.03
  }
}
```
</details>
