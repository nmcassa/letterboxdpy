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

<details>
  <summary>Click to expand demo response</summary>

```json
{
  "46911": {
    "slug": "children-of-men",
    "name": "Children of Men",
    "year": 2006,
    "url": "https://letterboxd.com/film/children-of-men/"
  },
  "16550": {
    "slug": "the-dark-knight-rises",
    "name": "The Dark Knight Rises",
    "year": 2012,
    "url": "https://letterboxd.com/film/the-dark-knight-rises/"
  },
  "48059": {
    "slug": "equilibrium",
    "name": "Equilibrium",
    "year": 2002,
    "url": "https://letterboxd.com/film/equilibrium/"
  }
}
```
</details>
