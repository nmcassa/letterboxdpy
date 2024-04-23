<h2 id="movie_watchers">movie_watchers(movie object)</h2>

```python
from letterboxdpy import movie
movie_instance = movie.Movie("v-for-vendetta")
print(movie.movie_watchers(movie_instance))
```

```json
{
    "watch_count": "981721",
    "fan_count": "8389",
    "like_count": "248662",
    "review_count": "35360",
    "list_count": "86666"
}
```