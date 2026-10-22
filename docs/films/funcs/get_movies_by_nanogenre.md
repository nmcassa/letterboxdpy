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

<details>
  <summary>Click to expand demo response</summary>

```json
{
  "51849": {
    "slug": "mad-max-fury-road",
    "name": "Mad Max: Fury Road",
    "year": 2015,
    "rating": 4.14,
    "url": "https://letterboxd.com/film/mad-max-fury-road/"
  },
  "51508": {
    "slug": "children-of-men",
    "name": "Children of Men",
    "year": 2006,
    "rating": 4.19,
    "url": "https://letterboxd.com/film/children-of-men/"
  },
  "51850": {
    "slug": "stalker",
    "name": "Stalker",
    "year": 1979,
    "rating": 4.38,
    "url": "https://letterboxd.com/film/stalker/"
  }
}
```
</details>
