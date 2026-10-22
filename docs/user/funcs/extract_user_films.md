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

<details>
  <summary>Click to expand demo response</summary>

```json
{
  "movies": {
    "street-fighter-2026": {
      "slug": "street-fighter-2026",
      "name": "Street Fighter",
      "year": 2026,
      "url": "https://letterboxd.com/film/street-fighter-2026/",
      "id": "1040290",
      "rating": 2.5,
      "liked": false
    },
    "the-social-reckoning": {
      "slug": "the-social-reckoning",
      "name": "The Social Reckoning",
      "year": 2026,
      "url": "https://letterboxd.com/film/the-social-reckoning/",
      "id": "1164669",
      "rating": 2.0,
      "liked": false
    },
    "digger-2026": {
      "slug": "digger-2026",
      "name": "Digger",
      "year": 2026,
      "url": "https://letterboxd.com/film/digger-2026/",
      "id": "1132688",
      "rating": 2.5,
      "liked": false
    }
  },
  "count": 767,
  "liked_count": 98,
  "rating_count": 707,
  "liked_percentage": 12.78,
  "rating_percentage": 92.18,
  "rating_average": 3.27
}
```
</details>
