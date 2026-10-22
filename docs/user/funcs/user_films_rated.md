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
    "the-matrix": {
      "name": "The Matrix",
      "id": "20593",
      "rating": 5.0,
      "liked": true
    },
    "interstellar": {
      "name": "Interstellar",
      "id": "117623",
      "rating": 5.0,
      "liked": true
    }
  },
  "count": 42,
  "liked_count": 39,
  "rating_count": 42,
  "liked_percentage": 92.86,
  "rating_percentage": 100.0,
  "rating_average": 10.0
}
```
</details>
