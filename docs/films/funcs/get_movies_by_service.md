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

<details>
  <summary>Click to expand demo response</summary>

```json
{
  "1629443": {
    "slug": "you-can-see-everything",
    "name": "You Can See Everything",
    "year": 2026,
    "url": "https://letterboxd.com/film/you-can-see-everything/",
    "rating": 4.65
  },
  "1139834": {
    "slug": "whalefall",
    "name": "Whalefall",
    "year": 2026,
    "url": "https://letterboxd.com/film/whalefall/",
    "rating": 3.24
  },
  "1040290": {
    "slug": "street-fighter-2026",
    "name": "Street Fighter",
    "year": 2026,
    "url": "https://letterboxd.com/film/street-fighter-2026/",
    "rating": 2.8
  }
}
```
</details>
