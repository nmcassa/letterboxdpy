
<h2 id="user_reviews">user_reviews(user object)</h2>

```python
from letterboxdpy import user
user_instance = user.User("nmcassa")
print(user.user_reviews(user_instance))
```

<details>
  <summary>Click to expand <code>user_reviews</code> method response</summary>

```json
{
    "reviews": {
        "495592379": {
            "movie": {
                "name": "Poor Things",
                "slug": "poor-things-2023",
                "id": "710352",
                "release": 2023,
                "link": "https://letterboxd.com/film/poor-things-2023/"
            },
            "type": "Watched",
            "no": 0,
            "link": "https://letterboxd.com/nmcassa/film/poor-things-2023/",
            "rating": 3.0,
            "review": {
                "content": "It looks like AI art and weird movie",
                "spoiler": false
            },
            "date": {
                "year": 2023,
                "month": 12,
                "day": 26
            },
            "page": 1
        },
        "152420824": {
            "movie": {
                "name": "I'm Thinking of Ending Things",
                "slug": "im-thinking-of-ending-things",
                "id": "430806",
                "release": 2020,
                "link": "https://letterboxd.com/film/im-thinking-of-ending-things/"
            },
            "type": "Watched",
            "no": 0,
            "link": "https://letterboxd.com/nmcassa/film/im-thinking-of-ending-things/",
            "rating": 4.0,
            "review": {
                "content": "yeah i dont get it",
                "spoiler": false
            },
            "date": {
                "year": 2021,
                "month": 2,
                "day": 14
            },
            "page": 1
        }
    },
    "count": 7,
    "last_page": 1
}
```
</details>