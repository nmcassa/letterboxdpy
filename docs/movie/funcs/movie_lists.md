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
  "limit": false,
  "count": 2,
  "last_page": 1,
  "lists": {
    "1234567": {
      "title": "Favorite Dystopian Films",
      "slug": "favorite-dystopian-films",
      "description": "Essential cinematic visions of authoritarian futures.",
      "url": "https://letterboxd.com/user/list/favorite-dystopian-films/",
      "count": 50,
      "likes": 342,
      "comments": 28
    },
    "7654321": {
      "title": "Graphic Novel Adaptations",
      "slug": "graphic-novel-adaptations",
      "description": "Movies adapted from comics and graphic novels.",
      "url": "https://letterboxd.com/user/list/graphic-novel-adaptations/",
      "count": 85,
      "likes": 190,
      "comments": 12
    }
  }
}
```
</details>
