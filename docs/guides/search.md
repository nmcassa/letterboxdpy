# Search Guide

The `Search` class provides full-text search capability across Letterboxd with support for category filters, result limits, pagination, and slug resolution.

---

## Basic Search

Search across all Letterboxd categories or restrict your query to a specific content type:

```python
from letterboxdpy.search import Search, SearchFilter

# 1. Search across all categories
search = Search("Dune")
print(f"Total results on page 1: {len(search.results['results'])}")

# 2. Search exclusively for films
film_search = Search("Dune", search_filter=SearchFilter.FILMS)
results = film_search.get_results(5)

for item in results.get("results", []):
    print(f"- {item.get('name')} ({item.get('year')}) -> {item.get('url')}")
```

??? example "Example `Search` Response Payload (`films` filter)"

    ```json
    {
      "available": true,
      "query": "Dune",
      "filter": "films",
      "end_page": 1,
      "count": 3,
      "results": [
        {
          "no": 1,
          "page": 1,
          "type": "film",
          "slug": "dune-2021",
          "name": "Dune",
          "year": 2021,
          "url": "https://letterboxd.com/film/dune-2021/",
          "poster": "https://a.ltrbxd.com/resized/film-poster/4/2/7/5/4/6/427546-dune-0-230-0-345-crop.jpg",
          "directors": [
            {
              "name": "Denis Villeneuve",
              "slug": "denis-villeneuve",
              "url": "https://letterboxd.com/director/denis-villeneuve/"
            }
          ]
        },
        {
          "no": 2,
          "page": 1,
          "type": "film",
          "slug": "dune-part-two",
          "name": "Dune: Part Two",
          "year": 2024,
          "url": "https://letterboxd.com/film/dune-part-two/",
          "poster": "https://a.ltrbxd.com/resized/film-poster/7/9/7/5/5/3/797553-dune-part-two-0-230-0-345-crop.jpg",
          "directors": [
            {
              "name": "Denis Villeneuve",
              "slug": "denis-villeneuve",
              "url": "https://letterboxd.com/director/denis-villeneuve/"
            }
          ]
        }
      ]
    }
    ```

---

## Available Filters

The `SearchFilter` enum provides 12 distinct search categories:

| Filter | Enum Value | Description |
| :--- | :--- | :--- |
| `SearchFilter.ALL` | `""` | Mixed results from all categories |
| `SearchFilter.FILMS` | `"films"` | Films, movies, documentaries |
| `SearchFilter.REVIEWS` | `"reviews"` | User-written reviews |
| `SearchFilter.LISTS` | `"lists"` | User-curated lists |
| `SearchFilter.ORIGINAL_LISTS` | `"original-lists"` | Original lists created on Letterboxd |
| `SearchFilter.STORIES` | `"stories"` | Letterboxd editorial articles & stories |
| `SearchFilter.CAST_CREW` | `"cast-crew"` | Actors, directors, and crew members |
| `SearchFilter.MEMBERS` | `"members"` | Letterboxd user profiles |
| `SearchFilter.TAGS` | `"tags"` | Member tags |
| `SearchFilter.ARTICLES` | `"articles"` | Journal articles |
| `SearchFilter.EPISODES` | `"episodes"` | Podcast episodes |
| `SearchFilter.FULL_TEXT` | `"full-text"` | Full-text content index |

```python
# Member search
member_search = Search("bugracoskun", search_filter=SearchFilter.MEMBERS)

# List search
list_search = Search("Cyberpunk", search_filter="lists")
```

??? example "Sample `Search` Response Payload (`members` Filter Mock)"

    ```json
    {
      "available": true,
      "query": "bugracoskun",
      "filter": "members",
      "end_page": 1,
      "count": 1,
      "results": [
        {
          "no": 1,
          "page": 1,
          "type": "member",
          "url": "https://letterboxd.com/bugracoskun/",
          "username": "bugracoskun",
          "display_name": "bugra",
          "badge": "patron",
          "avatar": {
            "exists": true,
            "upscaled": true,
            "url": "https://a.ltrbxd.com/resized/avatar/upload/sample_avatar.jpg"
          }
        }
      ]
    }
    ```

---

## Pagination & Limits

`Search` provides methods to control how much data is fetched:

```python
search = Search("Matrix", SearchFilter.FILMS)

# Fetch exact number of results (e.g. top 5)
top_5 = search.get_results(5)

# Fetch complete pages worth of results (e.g. 2 pages = 40 items)
two_pages = search.get_pages(2)

# Switch filters seamlessly without re-encoding query
cast_search = search.with_filter(SearchFilter.CAST_CREW)
```

---

## Resolving Film Slugs from Title

If you have a movie title string and need its canonical Letterboxd slug (for instance to initialize a `Movie` object), use `get_film_slug_from_title`:

```python
from letterboxdpy.search import get_film_slug_from_title
from letterboxdpy.movie import Movie

slug = get_film_slug_from_title("Inception 2010")
print(f"Resolved Slug: {slug}")  # "inception"

if slug:
    movie = Movie(slug)
    print(f"{movie.title} - Rating: {movie.rating}")
```

---

## API Reference

For detailed class and method documentation, see the [Search API Reference](../api/search.md).
