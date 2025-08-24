<h2 id="user_activity">get_activity()</h2>

```python
from letterboxdpy.user import User
user_instance = User("nmcassa")
print(user_instance.get_activity())
```

<details>
    <summary>Click to expand the demo response for <code>get_activity</code> method</summary>

```json
{
  "logs": {
    "9659817024": {
      "event_type": "review",
      "time": {
        "year": 2025,
        "month": 8,
        "day": 24,
        "hour": 14,
        "minute": 40,
        "second": 23
      }
    },
    "9624102431": {
      "event_type": "basic",
      "time": {
        "year": 2025,
        "month": 8,
        "day": 19,
        "hour": 16,
        "minute": 49,
        "second": 13
      },
      "log_type": "liked",
      "title": "nmcassa liked Ben Wold's review of Superman",
      "username": "ben24wold"
    },
    "9624100380": {
      "event_type": "basic",
      "time": {
        "year": 2025,
        "month": 8,
        "day": 19,
        "hour": 16,
        "minute": 48,
        "second": 50
      },
      "log_type": "added",
      "title": "nmcassa added The Substance to their watchlist"
    }
  },
  "total_logs": 20
}
```
</details>