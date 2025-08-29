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
  "metadata": {
    "export_timestamp": "2025-08-28T17:31:22.001861",
    "source_url": "https://letterboxd.com/ajax/activity-pagination/nmcassa",
    "total_activities": 3
  },
  "activities": {
    "9659817024": {
      "activity_type": "review",
      "timestamp": "2025-08-24T14:40:23.000000Z",
      "content": {
        "action": "watched",
        "description": "nmcassa watched and rated The Matrix ★★★★★",
        "movie": {
          "title": "The Matrix",
          "year": 1999,
          "slug": "the-matrix",
          "url": "https://letterboxd.com/film/the-matrix/"
        },
        "rating": 5.0
      }
    },
    "9624102431": {
      "activity_type": "basic",
      "timestamp": "2025-08-19T16:49:13.000000Z",
      "content": {
        "action": "liked",
        "description": "nmcassa liked Ben Wold's review of Superman",
        "movie": {
          "title": "Superman",
          "slug": "superman",
          "url": "https://letterboxd.com/film/superman/"
        }
      }
    },
    "9624100380": {
      "activity_type": "basic",
      "timestamp": "2025-08-19T16:48:50.000000Z",
      "content": {
        "action": "added",
        "description": "nmcassa added The Substance to their watchlist",
        "movie": {
          "title": "The Substance",
          "slug": "the-substance",
          "url": "https://letterboxd.com/film/the-substance/"
        }
      }
    }
  }
}
```
</details>