<h2 id="get_film_slug_from_title">get_film_slug_from_title(title: str) -> str</h2>

**Documentation:**

Searches for a film by title and returns its Letterboxd slug.

**Parameters:**
- `title` (str): The title of the film to search for

**Returns:**
- `str`: The film slug (e.g., "dune-2021") or `None` if not found

**Example:**
```python
from letterboxdpy.search import get_film_slug_from_title

# Get slug for a specific film
slug = get_film_slug_from_title("Dune")
print(slug)  # Output: "dune-2021"

# Handle case when film is not found  
slug = get_film_slug_from_title("NonexistentMovie123")
print(slug)  # Output: None
```

**Note:** This function returns the first search result. For more specific results, use the `Search` class directly.
