# Films & Discovery Guide

The `films` module provides discovery tools to explore movies on Letterboxd by release year, decade, genres, curated themes, upcoming releases, and streaming platforms.

---

## Generic `Films` Class

The `Films` class extracts movie lists from any valid Letterboxd catalog URL:

```python
from letterboxdpy.films import Films

# Browse all-time popular movies (limited to top 5)
popular = Films("https://letterboxd.com/films/popular/", max=5)

print(f"Total returned: {len(popular)}")
for film_id, film in popular.movies.items():
    print(f"- [{film_id}] {film['name']} ({film.get('year')}) - Rating: {film.get('rating')}")
```

??? example "Example `Films` Output Structure"

    ```json
    {
      "1197499": {
        "slug": "marty-supreme",
        "name": "Marty Supreme",
        "year": 2025,
        "rating": 4.21,
        "url": "https://letterboxd.com/film/marty-supreme/"
      },
      "772232": {
        "slug": "hamnet",
        "name": "Hamnet",
        "year": 2025,
        "rating": 4.22,
        "url": "https://letterboxd.com/film/hamnet/"
      }
    }
    ```

---

## Upcoming Releases

Fetch the most anticipated upcoming titles popular on Letterboxd:

```python
from letterboxdpy.films import get_upcoming_movies

upcoming = get_upcoming_movies(max=5)
for film_id, details in upcoming.items():
    print(f"- {details['name']} -> {details['url']}")
```

---

## Exploring by Year & Decade

Browse popular titles released in a specific calendar year or decade:

```python
from letterboxdpy.films import get_movies_by_year, get_movies_by_decade

# 1. By Decade (pass decade as 4-digit integer e.g. 1980, 1990, 2000)
eighties = get_movies_by_decade(1980, max=10)

# 2. By Calendar Year
films_2024 = get_movies_by_year(2024, max=10)
```

??? example "Example `get_movies_by_year(2024)` Output"

    ```json
    {
      "797553": {
        "slug": "dune-part-two",
        "name": "Dune: Part Two",
        "year": 2024,
        "rating": 4.51,
        "url": "https://letterboxd.com/film/dune-part-two/"
      },
      "834656": {
        "slug": "civil-war-2024",
        "name": "Civil War",
        "year": 2024,
        "rating": 3.65,
        "url": "https://letterboxd.com/film/civil-war-2024/"
      }
    }
    ```

---

## Exploring by Genre

Letterboxd categorizes movies under 19 official genres:

```python
from letterboxdpy.films import get_movies_by_genre

horror_movies = get_movies_by_genre("horror", max=10)
sci_fi = get_movies_by_genre("science-fiction", max=10)
```

| Supported Genre Slugs | | |
| :--- | :--- | :--- |
| `action` | `adventure` | `animation` |
| `comedy` | `crime` | `documentary` |
| `drama` | `family` | `fantasy` |
| `history` | `horror` | `music` |
| `mystery` | `romance` | `science-fiction` |
| `thriller` | `tv-movie` | `war` |
| `western` | | |

---

## Exploring by Streaming Service

Discover popular movies currently streaming on specific providers:

```python
from letterboxdpy.films import get_movies_by_service

netflix_films = get_movies_by_service("netflix", max=10)
criterion_films = get_movies_by_service("criterion-channel", max=10)
```

**Common service slugs:**
`netflix`, `criterion-channel`, `prime-video`, `hulu`, `disney-plus`, `apple-tv`, `hbo-max`, `peacock`, `mubi`.

---

## Curated Themes & Nanogenres

Letterboxd provides deep thematic taxonomies:

```python
from letterboxdpy.films import (
    get_movies_by_theme,
    get_movies_by_mini_theme,
    get_movies_by_nanogenre,
)

# Broad theme
epic_heroes = get_movies_by_theme("epic-heroes", max=5)

# Hyper-specific mini-theme
cyber_thrillers = get_movies_by_mini_theme("cyber-thriller-hacker", max=5)

# Nanogenre
nanogenre_films = get_movies_by_nanogenre("post-apocalyptic-survival", max=5)
```

---

## Terminal Formatting Helper

Use `print_movies` to quickly inspect lists in formatted terminal columns:

```python
from letterboxdpy.films import get_movies_by_year, print_movies

movies = get_movies_by_year(2024, max=5)
print_movies(movies, title="Top 2024 Movies")
```

---

## API Reference

For detailed function definitions, see the [Films Discovery API Reference](../api/films.md).
