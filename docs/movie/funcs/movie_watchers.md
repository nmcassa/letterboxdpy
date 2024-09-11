<h2 id="movie_watchers">movie_watchers(movie object)</h2>

```python
from letterboxdpy import movie
movie_instance = movie.Movie("v-for-vendetta")
print(movie.movie_watchers(movie_instance))
```

```json
{
    "members": 1090230,
    "fans": 9923,
    "likes": 278496,
    "reviews": 42180,
    "lists": 98866
}
```