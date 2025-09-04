<h2 id="user_films">user_films(user object)</h2>

```python
from letterboxdpy import user
user_instance = user.User("nmcassa")
print(user.user_films(user_instance))
```

<details>
    <summary>Click to expand the demo response for <code>user_films</code> method or <a href="/examples/exports/users/nmcassa/user_films.json" target="_blank">view the full response</a></summary>

```json
{
  "movies": {
    "civil-war-2024": {
      "name": "Civil War",
      "id": "834656",
      "rating": 3,
      "liked": false,
      "year": "2024"
    },
    "monkey-man": {
      "name": "Monkey Man",
      "id": "488751",
      "rating": 4.5,
      "liked": true,
      "year": "2024"
    },...
  },
  "count": 560,
  "liked_count": 80,
  "rating_count": 518,
  "liked_percentage": 14.29,
  "rating_percentage": 92.5,
  "rating_average": 3.24
}
```
</details>