<h2 id="user_diary">user_diary(user object)</h2>

```python
from letterboxdpy import user
user_instance = user.User("nmcassa")
print(user.user_diary(user_instance))
```

<details>
    <summary>Click to expand the demo response for <code>user_diary</code> method or <a href="/examples/exports/users/nmcassa/user_diary.json" target="_blank">view the full response</a></summary>

```json
{
    "entries": {
        "513520182": {
            "name": "Black Swan",
            "slug": "black-swan",
            "id": "20956",
            "release": 2010,
            "runtime": 108,
            "rewatched": false,
            "rating": 4.5,
            "liked": true,
            "reviewed": false,
            "date": {
                "year": 2024,
                "month": 1,
                "day": 15
            },
            "page": 1
        },...
        ...},
        "129707465": {
            "name": "mid90s",
            "slug": "mid90s",
            "id": "370451",
            "release": 2018,
            "runtime": 86,
            "rewatched": false,
            "rating": 4,
            "liked": false,
            "reviewed": false,
            "date": {
                "year": 2020,
                "month": 10,
                "day": 20
            },
            "page": 7
        }
    },
    "count": 337,
    "last_page": 7
}
```
</details>