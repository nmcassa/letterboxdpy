<h2 id="user_activity">user_activity(user object)</h2>

```python
from letterboxdpy import user
user_instance = user.User("nmcassa")
print(user.user_activity(user_instance))
```

<details>
    <summary>Click to expand the demo response for <code>user_activity</code> method or <a href="/examples/exports/users/nmcassa/user_activity.json" target="_blank">view the full response</a></summary>

```json
{
  "user": "nmcassa",
  "logs": {
    "6302725458": {
      "event_type": "basic",
      "time": {
        "year": 2024,
        "month": 1,
        "day": 30,
        "hour": 4,
        "minute": 7,
        "second": 42
      },
      "log_type": "watched",
      "title": "nmcassa   watched and rated  PlayTime   \u2605\u2605\u2605\u2605  on Monday Jan 29, 2024",
      "film": "PlayTime"
    },
    "6171883694": {
        "event_type": "review",
        "time": {
            "year": 2024,
            "month": 1,
            "day": 29,
            "hour": 12,
            "minute": 59,
            "second": 59
        },
        "event": "review",
        "type": "watched",
        "title": "nmcassa watched",
        "film": "example movie name",
        "film_year": 2000,
        "rating": 10,
        "spoiler": true,
        "review": "example review"
    },
    "6263706885": {
      "event_type": "basic",
      "time": {
        "year": 2024,
        "month": 1,
        "day": 23,
        "hour": 14,
        "minute": 32,
        "second": 12
      },
      "log_type": "liked",
      "title": "nmcassa liked L\u00e9o Barbosa\u2019s \ud83c\udfc6 Oscars 2024 list",
      "username": "000_leo"
    },...
}
```
</details>