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
  "51851": {
    "slug": "roma-2018",
    "name": "Roma",
    "year": 2018,
    "rating": 4.16,
    "url": "https://letterboxd.com/film/roma-2018/"
  },
  "51852": {
    "slug": "marriage-story",
    "name": "Marriage Story",
    "year": 2019,
    "rating": 4.02,
    "url": "https://letterboxd.com/film/marriage-story/"
  },
  "51854": {
    "slug": "the-irishman",
    "name": "The Irishman",
    "year": 2019,
    "rating": 3.91,
    "url": "https://letterboxd.com/film/the-irishman/"
  }
}
```
</details>
