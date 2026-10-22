<h2 id="movie_json">FilmURL.json(slug) & MovieJSON Data Model</h2>

Fetches raw structured movie JSON directly from Letterboxd's endpoint (`https://letterboxd.com/film/{slug}/json/`) and parses it into a strongly-typed `MovieJSON` dataclass.

```python
from letterboxdpy.url import FilmURL

# Fetch and deserialize into MovieJSON dataclass
movie_json = FilmURL.json("v-for-vendetta")

print(f"Title: {movie_json.name} ({movie_json.release_year})")
print(f"Letterboxd Numeric ID: {movie_json.id}")
print(f"Letterboxd LID: {movie_json.lid}")
print(f"Runtime: {movie_json.run_time} minutes")

for director in movie_json.directors:
    print(f"Director: {director.name}")
```

<details>
  <summary>Click to expand demo response</summary>

```json
{
  "result": true,
  "csrf": "<redacted>",
  "lid": "29Ik",
  "uid": "film:51400",
  "type": "film",
  "type_name": "film",
  "id": 51400,
  "name": "V for Vendetta",
  "image_125": "/film/v-for-vendetta/image-125/",
  "image_150": "/film/v-for-vendetta/image-150/",
  "release_year": 2005,
  "run_time": 132,
  "slug": "v-for-vendetta",
  "url": "/film/v-for-vendetta/",
  "original_name": null,
  "filmlist_action": "null",
  "watchlist_action": "/film/v-for-vendetta/add-to-watchlist/",
  "directors": [
    {
      "name": "James McTeigue"
    }
  ]
}
```
</details>

### MovieJSON Dataclass Fields

- `id` (int): Numeric Letterboxd film ID.
- `lid` (str): Short Letterboxd ID (e.g. `"dfdk"`).
- `uid` (str): Prefixed ID (e.g. `"film:315675"`).
- `name` (str): English or primary title.
- `original_name` (str | None): Original non-English title if applicable.
- `release_year` (int): Year of release.
- `run_time` (int): Film duration in minutes.
- `slug` (str): Film URL slug.
- `url` (str): Relative URL path.
- `image_125` / `image_150` (str): Relative poster paths.
- `directors` (list[Director]): List of director objects with `.name`.
- `result` (bool): API result flag.
- `csrf` (str): Letterboxd CSRF token.
- `filmlist_action` / `watchlist_action` (str): Action endpoint paths.
