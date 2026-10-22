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
    "civil-war-2024": {
      "name": "Civil War",
      "id": "834656",
      "rating": 1.5,
      "liked": false
    },
    "monkey-man": {
      "name": "Monkey Man",
      "id": "488751",
      "rating": 4.5,
      "liked": true
    }
  },
  "count": 560,
  "liked_count": 80,
  "rating_count": 518,
  "liked_percentage": 14.29,
  "rating_percentage": 92.5,
  "rating_average": 6.47
}
```
</details>
