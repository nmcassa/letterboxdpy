<h2 id="movie_lists">get_lists() -> dict</h2>

Fetches public Letterboxd lists containing the movie.

```python
from letterboxdpy.movie import Movie

movie_instance = Movie("v-for-vendetta")
lists_data = movie_instance.get_lists()

print(f"Lists found: {lists_data['count']}")
for list_id, item in lists_data["lists"].items():
    print(f"- {item['title']} ({item['count']} films)")
```

<details>
  <summary>Click to expand demo response</summary>

```json
{
  "limit": true,
  "count": 3,
  "last_page": 1,
  "lists": {
    "78954401": {
      "title": "Movies everyone should watch at least once during their lifetime",
      "slug": "movies-everyone-should-watch-at-least-once-1",
      "description": "",
      "url": "https://letterboxd.com/sloppyfeet/list/movies-everyone-should-watch-at-least-once-1/",
      "count": 767,
      "likes": 0,
      "comments": 0
    },
    "76273618": {
      "title": "Download List",
      "slug": "download-list",
      "description": "",
      "url": "https://letterboxd.com/danielpica/list/download-list/",
      "count": 858,
      "likes": 0,
      "comments": 0
    },
    "79248004": {
      "title": "Director Jim's Top Movies",
      "slug": "director-jims-top-movies",
      "description": "",
      "url": "https://letterboxd.com/jhawley07/list/director-jims-top-movies/",
      "count": 1127,
      "likes": 1,
      "comments": 0
    }
  }
}
```
</details>
