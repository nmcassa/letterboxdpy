# List Guide

The `List` class allows extracting metadata, film entries, creation dates, tags, and notes from any user-curated Letterboxd list.

---

## Quick Example

```python
from letterboxdpy.list import List

# Initialize using list author username and list slug
film_list = List("bugracoskun", "cold-palettes-dark-cities")

print(f"Title: {film_list.title}")
print(f"Author: {film_list.author}")
print(f"Total Films: {film_list.count}")
print(f"Created: {film_list.date_created}")
print(f"Updated: {film_list.date_updated}")
print(f"Tags: {film_list.tags}")
print(f"Description: {film_list.description}")
```

??? example "Sample `List` Payload Structure (Mock Demonstration)"

    ```json
    {
      "username": "bugracoskun",
      "slug": "cold-palettes-dark-cities",
      "list_id": "10000001",
      "title": "cold palettes, dark cities",
      "author": "bugra",
      "url": "https://letterboxd.com/bugracoskun/list/cold-palettes-dark-cities/",
      "count": 25,
      "date_created": "2025-01-01T00:00:00.000000Z",
      "date_updated": "2025-06-01T00:00:00.000000Z",
      "description": "Sample curated list demonstrating movie collection responses.",
      "tags": [
        "atmosphere",
        "neo-noir",
        "sample-list"
      ],
      "_movies": {
        "51345": {
          "slug": "se7en",
          "name": "Se7en",
          "year": 1995,
          "url": "https://letterboxd.com/film/se7en/"
        },
        "47104": {
          "slug": "the-crow",
          "name": "The Crow",
          "year": 1994,
          "url": "https://letterboxd.com/film/the-crow/"
        },
        "...": "..."
      }
    }
    ```

---

## Accessing and Iterating Films

The `.movies` property uses **lazy loading**; film entries are fetched and parsed from Letterboxd only upon first access, and cached for subsequent calls:

```python
# len() returns total films count
print(f"List size: {len(film_list)}")

# Iterate over movies dictionary
for movie_id, film in film_list.movies.items():
    print(f"- [{movie_id}] {film['name']} ({film['year']})")
    print(f"  URL: {film['url']}")
```

---

## List Metadata Reference

| Property | Type | Description |
| :--- | :--- | :--- |
| `list_id` | `str` | Unique numeric identifier for the list on Letterboxd |
| `title` | `str` | Human-readable title of the list |
| `author` | `str` | Letterboxd username of the creator |
| `url` | `str` | Canonical web URL of the list |
| `count` | `int` | Total number of film entries |
| `date_created`| `str` | ISO 8601 creation timestamp |
| `date_updated`| `str` | ISO 8601 last modified timestamp |
| `description` | `str` | Optional markdown/text notes attached to the list |
| `tags` | `list[str]` | Custom user tags assigned to the list |
| `movies` | `dict` | Dictionary mapping `movie_id` to movie dictionaries |

---

## API Reference

For detailed function definitions, see the [List API Reference](../api/list.md).
