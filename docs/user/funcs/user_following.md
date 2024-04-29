<h2 id="user_following">user_following(user object)</h2>

```python
from letterboxdpy import user
user_instance = user.User("nmcassa")
print(user.user_following(user_instance))
```

<details>
  <summary>Click to expand <code>user_following</code> method response</summary>

```json
{
    "ppark": {
        "display_name": "ppark"
    },
    "ryanshubert": {
        "display_name": "ryanshubert"
    },
    "crescendohouse": {
        "display_name": "Crescendo House"
    },...
}
```
</details>