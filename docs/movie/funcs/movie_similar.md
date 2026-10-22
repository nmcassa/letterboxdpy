<h2 id="movie_similar">get_similar_movies() -> dict</h2>

Fetches recommended and similar films for the movie from Letterboxd.

```python
from letterboxdpy.movie import Movie

movie_instance = Movie("v-for-vendetta")
similar_movies = movie_instance.get_similar_movies()

for movie_id, film in similar_movies.items():
    print(f"- {film['name']} ({film.get('rating', 'unrated')})")
```

<details>
  <summary>Click to expand demo response</summary>

```json
{
  "51568": {
    "slug": "fight-club",
    "name": "Fight Club",
    "year": 1999,
    "url": "https://letterboxd.com/film/fight-club/",
    "rating": 4.27
  },
  "371378": {
    "slug": "dune-2021",
    "name": "Dune",
    "year": 2021,
    "url": "https://letterboxd.com/film/dune-2021/",
    "rating": 3.89
  },
  "51896": {
    "slug": "the-dark-knight",
    "name": "The Dark Knight",
    "year": 2008,
    "url": "https://letterboxd.com/film/the-dark-knight/",
    "rating": 4.5
  }
}
```
</details>
