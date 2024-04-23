<h2 id="user_tags">user_tags(user object)</h2>

```python
from letterboxdpy import user
user_instance = user.User("nmcassa")
result = user.user_tags(user_instance)
print(result)
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
