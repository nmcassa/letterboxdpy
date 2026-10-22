<h2 id="user_films">get_films() -> dict</h2>

Fetches all watched films and metadata for the user.

```python
from letterboxdpy.user import User

user_instance = User("nmcassa")

# Get all watched films
films_data = user_instance.get_films()
print(f"Total watched: {films_data['count']}")

# Filter films by score (e.g. 5-star films)
five_stars = user_instance.get_films_by_rating(5.0)

# Unrated films
unrated = user_instance.get_films_not_rated()
```

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