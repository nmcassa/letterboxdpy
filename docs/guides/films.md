# Films & Discovery Guide

`letterboxdpy` provides discovery functions to explore films on Letterboxd by streaming service, release year, decade, genres, and curated themes.

---

## Exploring by Genre & Themes

```python
from letterboxdpy.films import (
    get_movies_by_genre,
    get_movies_by_theme,
    get_movies_by_mini_theme,
    get_upcoming_movies,
)

# 1. By Genre
horror_films = get_movies_by_genre("horror", max=10)

# 2. By Theme
epic_heroes = get_movies_by_theme("epic-heroes", max=5)

# 3. By Mini-Theme
democracy_films = get_movies_by_mini_theme(
    "politician-assassination-democracy-president-compelling", 
    max=5
)

# 4. Upcoming releases
upcoming = get_upcoming_movies(max=5)
```

??? example "Example Discovery Payload Structure"

    ```json
    {
      "1197499": {
        "slug": "marty-supreme",
        "name": "Marty Supreme",
        "rating": 4.21,
        "url": "https://letterboxd.com/film/marty-supreme/"
      },
      "772232": {
        "slug": "hamnet",
        "name": "Hamnet",
        "rating": 4.22,
        "url": "https://letterboxd.com/film/hamnet/"
      }
    }
    ```

---

## Exploring by Year & Decade

```python
from letterboxdpy.films import get_movies_by_decade, get_movies_by_year

# Popular 1980s movies
eighties_films = get_movies_by_decade(1980, max=10)

# Popular 2024 movies
films_2024 = get_movies_by_year(2024, max=10)
```

---

## Exploring by Streaming Service

```python
from letterboxdpy.films import get_movies_by_service

# What's popular on streaming
netflix_popular = get_movies_by_service("netflix", max=10)
criterion_popular = get_movies_by_service("criterion-channel", max=10)
```

---

## API Reference

For detailed function definitions, see the [Films Discovery API Reference](../api/films.md).
