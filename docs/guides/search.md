# Search Guide

The `Search` class provides full-text search capability across Letterboxd with support for filters and pagination.

---

## Basic Search

```python
from letterboxdpy.search import Search, SearchFilter

# Search across all categories
search = Search("Dune")

print(f"Total results on page 1: {len(search.results['results'])}")
```

??? example "Example `Search` Payload"

    ```json
    {
      "available": true,
      "query": "Dune",
      "filter": "films",
      "end_page": 1,
      "count": 5,
      "results": [
        {
          "no": 1,
          "page": 1,
          "type": "film",
          "slug": "dune-2021",
          "name": "Dune",
          "year": 2021,
          "url": "https://letterboxd.com/film/dune-2021/",
          "directors": [
            {
              "name": "Denis Villeneuve",
              "slug": "denis-villeneuve"
            }
          ]
        }
      ]
    }
    ```

---

## Filtering Results

Use the `SearchFilter` enum or strings to narrow down your query:

```python
# Search exclusively for films
film_search = Search("Dune", search_filter=SearchFilter.FILMS)

# Search for members/users
member_search = Search("nmcassa", search_filter=SearchFilter.MEMBERS)

# Search for user lists
list_search = Search("Cyberpunk", search_filter=SearchFilter.LISTS)

# Search for reviews
review_search = Search("Oppenheimer", search_filter=SearchFilter.REVIEWS)
```

---

## Available Filters

- `SearchFilter.ALL` (`""`)
- `SearchFilter.FILMS` (`"films"`)
- `SearchFilter.REVIEWS` (`"reviews"`)
- `SearchFilter.LISTS` (`"lists"`)
- `SearchFilter.ORIGINAL_LISTS` (`"original-lists"`)
- `SearchFilter.STORIES` (`"stories"`)
- `SearchFilter.CAST_CREW` (`"cast-crew"`)
- `SearchFilter.MEMBERS` (`"members"`)
- `SearchFilter.TAGS` (`"tags"`)

---

## API Reference

For detailed function definitions, see the [Search API Reference](../api/search.md).
