<h2 id="movie_watchers">get_watchers_stats() -> dict</h2>

Fetches member activity statistics for the movie (members, fans, likes, reviews, and list appearances) from the `/members/` subpage.

```python
from letterboxdpy.movie import Movie

movie_instance = Movie("v-for-vendetta")
watchers = movie_instance.get_watchers_stats()
print(watchers)
```

<details>
  <summary>Click to expand demo response</summary>

```json
{
    "members": 1090230,
    "fans": 9923,
    "likes": 278496,
    "reviews": 42180,
    "lists": 98866
}
```
</details>