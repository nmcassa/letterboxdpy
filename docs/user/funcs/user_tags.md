<h2 id="get_user_tags">get_user_tags() -> dict</h2>

```python
from letterboxdpy.user import User

user_instance = User("nmcassa")
result = user_instance.get_user_tags()
print(f"Total tag references: {result['count']}")
```

<details>
  <summary>Click to expand <code>user_tags</code> method response</summary>

```json
{
  "films": {"tags": {"lol": {...}}, "count": 1},
  "diary": {"tags": {"lol": {...}}, "count": 1},
  "reviews": {"tags": {"lol": {...}}, "count": 1},
  "lists": {
    "tags": {
      "hacking": {
        "name": "hacking",
        "title": "hacking",
        "link": "/nmcassa/tag/hacking/lists/",
        "count": 1,
        "no": 1
      }
    },
    "count": 1
  },
  "count": 4
}
```
</details>
