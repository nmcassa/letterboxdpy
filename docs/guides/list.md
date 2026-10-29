# List Guide

The `List` class allows extracting metadata, film entries, authors, and notes from any user-curated Letterboxd list.

---

## Quick Example

```python
from letterboxdpy.list import List

# Initialize with author username and list slug
film_list = List("nmcassa", "movies-to-watch-with-priscilla-park")

print(f"Title: {film_list.title}")
print(f"Author: {film_list.author}")
print(f"Total Films: {film_list.count}")
print(f"Description: {film_list.description}")
```

??? example "Example `List` Payload Structure"

    ```json
    {
      "username": "nmcassa",
      "slug": "movies-to-watch-with-priscilla-park",
      "url": "https://letterboxd.com/nmcassa/list/movies-to-watch-with-priscilla-park",
      "list_id": "31052453",
      "title": "Movies to Watch with Priscilla Park",
      "author": "nmcassa",
      "count": 2,
      "date_created": "2024-05-18T16:44:57.013000Z",
      "date_updated": "2024-05-20T14:58:06.486000Z",
      "description": null,
      "tags": [],
      "_movies": {
        "240344": {
          "slug": "la-la-land",
          "name": "La La Land",
          "year": 2016,
          "url": "https://letterboxd.com/film/la-la-land/"
        }
      }
    }
    ```

---

## Iterating Over Movies

A `List` instance can be iterated or accessed like a collection:

```python
# Number of films
total = len(film_list)

# Access all movies dictionary
for slug, movie in film_list.movies.items():
    print(f"- {movie['name']} ({movie['year']}) -> {movie['url']}")
```

---

## List Metadata

Available properties on a `List` instance:

- `film_list.list_id`: Unique numeric Letterboxd list ID
- `film_list.title`: List title
- `film_list.author`: List creator's username
- `film_list.url`: Canonical Letterboxd URL
- `film_list.count`: Total count of films in the list
- `film_list.date_created`: Creation timestamp (ISO 8601)
- `film_list.date_updated`: Last modified timestamp (ISO 8601)
- `film_list.description`: Full text description / list notes
- `film_list.tags`: List of tags assigned to the list

---

## API Reference

For detailed function definitions, see the [List API Reference](../api/list.md).
