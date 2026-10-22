<h2 id="extract_user_films">extract_user_films(url: str) -> dict</h2>

Extracts user films and summary statistics from a Letterboxd films URL.

```python
from letterboxdpy.pages.user_films import extract_user_films

# Scrape from a user's watched films page
data = extract_user_films("https://letterboxd.com/nmcassa/films/")

print(f"Total films: {data['count']}")
print(f"Liked films: {data['liked_count']}")
print(f"Average rating: {data['rating_average']}")
```

**Parameters:**
- `url` (str): Full URL to the user's films page or filtered view.

**Returns:**
- `dict`: Dictionary containing `movies`, `count`, `liked_count`, `rating_count`, `liked_percentage`, `rating_percentage`, and `rating_average`.
