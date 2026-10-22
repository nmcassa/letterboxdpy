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
