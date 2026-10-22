<h2 id="get_movies_by_similar">Similar Movies Overview</h2>

Similar movie recommendations on Letterboxd are accessible via the `Movie` class or `Films` scraper:

```python
from letterboxdpy.movie import Movie

# Recommended: Use Movie.get_similar_movies()
movie_instance = Movie("v-for-vendetta")
similar_movies = movie_instance.get_similar_movies()

for movie_id, film in similar_movies.items():
    print(f"- {film['name']} ({film.get('rating')})")
```

Alternatively, scrape the endpoint directly with `Films`:

```python
from letterboxdpy.films import Films

films = Films("https://letterboxd.com/film/v-for-vendetta/similar/", max=10)
print(films.movies)
```
