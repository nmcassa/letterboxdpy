<h2 id="user_wrapped">user_wrapped(user object)</h2>

```python
from letterboxdpy import user
user_instance = user.User("nmcassa")
print(user.user_wrapped(user_instance, 2023))
```

<details>
    <summary>Click to expand the demo response for <code>user_wrapped</code> method or <a href="/examples/exports/users/nmcassa/user_wrapped.json" target="_blank">view the full response</a></summary>

```json
{
    "year": 2023,
    "logged": 120,
    "total_review": 2,
    "hours_watched": 223,
    "total_runtime": 13427,
    "first_watched": {
        "332289592": {
            "name": "The Gift",
            "slug": "the-gift-2015-1",
            "id": "255927",
            "release": 2015,
            "runtime": 108,
            "actions": {
                "rewatched": false,
                "rating": 6,
                "liked": false,
                "reviewed": false
            },
            "date": {
                "year": 2023,
                "month": 1,
                "day": 1
            },
            "page": {
                "url": "https://letterboxd.com/nmcassa/films/diary/for/2023/page/3/",
                "no": 3
            }
        }
    },
    "last_watched": {
        "495592379": {...}
    },
    "movies": {
        "495592379": {
            "name": "Poor Things",
            "slug": "poor-things-2023",
            "id": "710352",
            "release": 2023,
            "runtime": 141,
            "actions": {
                "rewatched": false,
                "rating": 6,
                "liked": false,
                "reviewed": true
            },
            "date": {
                "year": 2023,
                "month": 12,
                "day": 26
            },
            "page": {
                "url": "https://letterboxd.com/nmcassa/films/diary/for/2023/page/1/",
                "no": 1
            }
        },...
    },
    "months": {
        "1": 21,
        "2": 7,
        "3": 7,
        "4": 6,
        "5": 11,
        "6": 9,
        "7": 15,
        "8": 11,
        "9": 5,
        "10": 9,
        "11": 7,
        "12": 12
    },
    "days": {
        "1": 18,
        "2": 14,
        "3": 9,
        "4": 17,
        "5": 14,
        "6": 27,
        "7": 21
    },
    "milestones": {
        "50": {
            "413604382": {
                "name": "Richard Pryor: Live in Concert",
                "slug": "richard-pryor-live-in-concert",
                "id": "37594",
                "release": 1979,
                "runtime": 78,
                "actions": {
                    "rewatched": false,
                    "rating": 7,
                    "liked": false,
                    "reviewed": false
                },
                "date": {
                    "year": 2023,
                    "month": 7,
                    "day": 13
                },
                "page": {
                    "url": "https://letterboxd.com/nmcassa/films/diary/for/2023/page/1/",
                    "no": 1
                }
            }
        },
        "100": {
            "347318246": {...}
        }
    }
}
```
</details>