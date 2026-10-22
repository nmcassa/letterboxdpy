<h2 id="movie_lists">get_lists() -> dict</h2>

Fetches public Letterboxd lists containing the movie.

```python
from letterboxdpy.movie import Movie

movie_instance = Movie("v-for-vendetta")
lists_data = movie_instance.get_lists()

print(f"Lists found: {len(lists_data)}")
for list_id, item in lists_data.items():
    print(f"- {item['title']} by {item.get('author', 'unknown')}")
```
