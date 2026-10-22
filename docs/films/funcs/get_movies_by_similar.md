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
  "51508": {
    "slug": "children-of-men",
    "name": "Children of Men",
    "year": 2006,
    "rating": 4.19,
    "url": "https://letterboxd.com/film/children-of-men/"
  },
  "51401": {
    "slug": "equilibrium",
    "name": "Equilibrium",
    "year": 2002,
    "rating": 3.44,
    "url": "https://letterboxd.com/film/equilibrium/"
  },
  "51842": {
    "slug": "dark-city",
    "name": "Dark City",
    "year": 1998,
    "rating": 3.82,
    "url": "https://letterboxd.com/film/dark-city/"
  }
}
```
</details>
