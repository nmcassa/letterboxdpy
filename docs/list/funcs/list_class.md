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
