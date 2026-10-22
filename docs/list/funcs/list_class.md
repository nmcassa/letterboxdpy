<h2 id="list_class">List Class (User Lists)</h2>

Provides access to Letterboxd lists, list metadata, and movie items with lazy loading.

```python
from letterboxdpy.list import List

# Instantiate with username and list slug
list_instance = List("nmcassa", "movies-to-watch-with-priscilla-park")

print(f"Title: {list_instance.title}")
print(f"Author: {list_instance.author}")
print(f"Total films: {list_instance.count}")
print(f"Created: {list_instance.date_created}")
print(f"Updated: {list_instance.date_updated}")

# Access movies (lazy-loaded property)
for movie_id, film in list_instance.movies.items():
    print(f"- {film['name']} ({film['year']})")
```

<details>
  <summary>Click to expand demo response</summary>

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
  "movies": {
    "240344": {
      "slug": "la-la-land",
      "name": "La La Land",
      "year": 2016,
      "url": "https://letterboxd.com/film/la-la-land/"
    },
    "703077": {
      "slug": "magazine-dreams",
      "name": "Magazine Dreams",
      "year": 2023,
      "url": "https://letterboxd.com/film/magazine-dreams/"
    }
  }
}
```
</details>

### Attributes & Properties

- `username` (str): Author's username.
- `slug` (str): List URL slug.
- `list_id` (str): Numeric list ID.
- `title` (str): List title.
- `author` (str): Author display name / username.
- `url` (str): Canonical URL.
- `count` (int): Number of films in list.
- `date_created` (list/str): ISO creation timestamp.
- `date_updated` (list/str): ISO update timestamp.
- `description` (str | None): List description text.
- `tags` (list): User-assigned tags.
- `movies` (dict): Dictionary mapping film IDs to movie metadata (`slug`, `name`, `year`, `url`).
