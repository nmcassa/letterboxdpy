<h2 id="user_liked_reviews">user_liked_reviews(user object)</h2>

```python
from letterboxdpy import user
user_instance = user.User("nmcassa")
print(user.user_liked_reviews(user_instance))
```

<details>
  <summary>Click to expand <code>user_liked_reviews</code> method response</summary>

```json
{
    "reviews": {
        "666730921": {
            "type": "Rewatched",
            "no": 0,
            "url": "https://letterboxd.com/ppark/film/mean-girls/",
            "rating": 8,
            "review": {
                "content": "Refreshing",
                "spoiler": false,
                "date": {
                    "year": 2024,
                    "month": 9,
                    "day": 7
                }
            },
            "user": {
                "username": "ppark",
                "display_name": "ppark",
                "url": "https://letterboxd.com/ppark/"
            },
            "movie": {
                "name": "Mean Girls",
                "slug": "mean-girls",
                "id": "46049",
                "release": 2004,
                "url": "https://letterboxd.com/film/mean-girls/"
            },
            "page": 1
        },
        ...
        "80658991": {
            "type": "Added",
            "no": 0,
            "url": "https://letterboxd.com/kurstboy/film/the-departed/",
            "rating": 9,
            "review": {
                "content": "Great way to end my Scorsese binge!That final shot is perfect and the whole third act feels tight as hell. The entire film is rich with interesting approaches to the subject matter which is fitting for a plot that grabs your attention within the first 5 minutes. Scorsese is just spitballing here and throwing every idea at the wall, his love for filmmaking shines brighter here than in something like Hugo. Don't know what to add to the table\u2026",
                "spoiler": false,
                "date": {
                    "year": 2019,
                    "month": 11,
                    "day": 24
                }
            },
            "user": {
                "username": "Kurstboy",
                "display_name": "Karsten",
                "url": "https://letterboxd.com/kurstboy/"
            },
            "movie": {
                "name": "The Departed",
                "slug": "the-departed",
                "id": "51042",
                "release": 2006,
                "url": "https://letterboxd.com/film/the-departed/"
            },
            "page": 2
        }
    }
}
```
</details>