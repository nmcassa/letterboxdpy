# Movie Guide

The `Movie` class fetches metadata, statistics, reviews, cast, crew, and recommendations for films on Letterboxd.

---

## Initialization

Initialize a `Movie` instance using a Letterboxd slug or external identifier (TMDB ID or IMDb ID):

```python
from letterboxdpy.movie import Movie

# 1. By slug
movie = Movie("v-for-vendetta")

# 2. By TMDB ID
movie_tmdb = Movie.from_tmdb(752)

# 3. By IMDb ID
movie_imdb = Movie.from_imdb("tt0434409")
```

??? example "Example `Movie` Payload Structure"

    ```json
    {
      "url": "https://letterboxd.com/film/v-for-vendetta/",
      "slug": "v-for-vendetta",
      "id": "51400",
      "title": "V for Vendetta",
      "year": 2005,
      "runtime": 132,
      "rating": 3.84,
      "tmdb_id": "752",
      "imdb_id": "tt0434409",
      "poster": "https://a.ltrbxd.com/resized/film-poster/5/1/4/0/0/51400-v-for-vendetta-0-230-0-345-crop.jpg",
      "tagline": "People should not be afraid of their governments.",
      "description": "In a world in which Great Britain has become a fascist state...",
      "genres": [
        {"name": "Action", "slug": "action"},
        {"name": "Thriller", "slug": "thriller"}
      ],
      "crew": {
        "director": [{"name": "James McTeigue", "slug": "james-mcteigue"}]
      }
    }
    ```

---

## Related Endpoints

### Similar Movies

```python
similar = movie.pages.similar.get_similar_movies()
```

??? example "Example `similar` Payload"

    ```json
    {
      "count": 12,
      "movies": {
        "equilibrium": {
          "name": "Equilibrium",
          "year": 2002,
          "url": "https://letterboxd.com/film/equilibrium/"
        },
        "children-of-men": {
          "name": "Children of Men",
          "year": 2006,
          "url": "https://letterboxd.com/film/children-of-men/"
        }
      }
    }
    ```

### Watchers and Fan Statistics

```python
stats = movie.pages.members.get_watchers_stats()
```

---

## API Reference

For detailed function definitions, parameters, and return types, see the [Movie API Reference](../api/movie.md).
