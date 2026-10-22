<h2 id="get_liked_films">get_liked_films() -> dict</h2>

Fetches all films marked as liked by the user.

```python
from letterboxdpy.user import User

user_instance = User("nmcassa")
liked_films = user_instance.get_liked_films()

print(f"Total liked films: {liked_films['count']}")
for slug, movie in liked_films['movies'].items():
    print(f"- {movie['name']} ({movie.get('year', 'N/A')})")
```

**Returns:**
- `dict`: A dictionary containing `count`, `movies` (dict mapping film slug to movie metadata), and pagination details.

<details>
  <summary>Click to expand demo response</summary>

```json
{
  "movies": {
    "monkey-man": {
      "name": "Monkey Man",
      "id": "488751",
      "rating": 4.5,
      "liked": true
    },
    "poor-things-2023": {
      "name": "Poor Things",
      "id": "710352",
      "rating": 4.0,
      "liked": true
    }
  },
  "count": 80,
  "liked_count": 80,
  "rating_count": 78,
  "liked_percentage": 100.0,
  "rating_percentage": 97.5,
  "rating_average": 7.82
}
```
</details>
