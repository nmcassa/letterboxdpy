<h2 id="get_films_by_rating">get_films_by_rating(rating: float | int) -> dict</h2>

Fetches films given a specific star rating by the user (from 0.5 to 5.0).

```python
from letterboxdpy.user import User

user_instance = User("nmcassa")

# Fetch all 5-star films
five_star_films = user_instance.get_films_by_rating(5.0)
print(f"5-star count: {five_star_films['count']}")

# Fetch unrated films
unrated = user_instance.get_films_not_rated()
print(f"Unrated count: {unrated['count']}")
```

**Parameters:**
- `rating` (float | int): Rating score between 0.5 and 5.0 in half-star increments.

**Returns:**
- `dict`: Movies dictionary matching the rating with count and pagination details.

<details>
  <summary>Click to expand demo response</summary>

```json
{
  "movies": {
    "the-odyssey-2026": {
      "slug": "the-odyssey-2026",
      "name": "The Odyssey",
      "year": 2026,
      "url": "https://letterboxd.com/film/the-odyssey-2026/",
      "id": "1255394",
      "rating": 5.0,
      "liked": false
    },
    "one-battle-after-another": {
      "slug": "one-battle-after-another",
      "name": "One Battle After Another",
      "year": 2025,
      "url": "https://letterboxd.com/film/one-battle-after-another/",
      "id": "951277",
      "rating": 5.0,
      "liked": true
    },
    "walle": {
      "slug": "walle",
      "name": "WALL·E",
      "year": 2008,
      "url": "https://letterboxd.com/film/walle/",
      "id": "45994",
      "rating": 5.0,
      "liked": true
    }
  },
  "count": 38,
  "liked_count": 33,
  "rating_count": 38,
  "liked_percentage": 86.84,
  "rating_percentage": 100.0,
  "rating_average": 5.0
}
```
</details>
