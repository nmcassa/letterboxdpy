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
    "you-can-see-everything": {
      "slug": "you-can-see-everything",
      "name": "You Can See Everything",
      "year": 2026,
      "url": "https://letterboxd.com/film/you-can-see-everything/",
      "id": "1629443",
      "rating": 4.5,
      "liked": true
    },
    "project-hail-mary": {
      "slug": "project-hail-mary",
      "name": "Project Hail Mary",
      "year": 2026,
      "url": "https://letterboxd.com/film/project-hail-mary/",
      "id": "611288",
      "rating": 4.5,
      "liked": true
    },
    "send-help": {
      "slug": "send-help",
      "name": "Send Help",
      "year": 2026,
      "url": "https://letterboxd.com/film/send-help/",
      "id": "1084117",
      "rating": 4.5,
      "liked": true
    }
  },
  "count": 98,
  "liked_count": 98,
  "rating_count": 97,
  "liked_percentage": 100.0,
  "rating_percentage": 98.98,
  "rating_average": 4.55
}
```
</details>
