<h2 id="movie_similar">get_similar_movies() -> dict</h2>

Fetches recommended and similar films for the movie from Letterboxd.

```python
from letterboxdpy.movie import Movie

movie_instance = Movie("v-for-vendetta")
similar_movies = movie_instance.get_similar_movies()

for movie_id, film in similar_movies.items():
    print(f"- {film['name']} ({film.get('rating', 'unrated')})")
```
