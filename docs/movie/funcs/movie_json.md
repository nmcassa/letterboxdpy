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
  "csrf": "a1b2c3d4e5f6...",
  "lid": "16f4",
  "uid": "film:51400",
  "type": "film",
  "typeName": "film",
  "id": 51400,
  "name": "V for Vendetta",
  "originalName": null,
  "image125": "/resized/film-poster/5/1/4/0/0/51400-v-for-vendetta-0-125-0-187-crop.jpg",
  "image150": "/resized/film-poster/5/1/4/0/0/51400-v-for-vendetta-0-150-0-225-crop.jpg",
  "releaseYear": 2005,
  "runTime": 132,
  "slug": "v-for-vendetta",
  "url": "/film/v-for-vendetta/",
  "filmlistAction": "/film/v-for-vendetta/mark-as-watched/",
  "watchlistAction": "/film/v-for-vendetta/mark-as-want/",
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
