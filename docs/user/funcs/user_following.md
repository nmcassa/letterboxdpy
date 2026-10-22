<h2 id="get_following">get_following(page=1, limit=None) -> dict</h2>

Fetches a dictionary of users followed by the given account, including social metrics and avatars.

```python
from letterboxdpy.user import User

user_instance = User("nmcassa")

# Fetch first page of following
following = user_instance.get_following()
print(f"Following count on page 1: {len(following)}")

# Fetch specific page or limit results
following_p2 = user_instance.get_following(page=2, limit=50)
```

**Parameters:**
- `page` (int, optional): Page number to start fetching from. Defaults to 1.
- `limit` (int, optional): Maximum number of pages to fetch.

<details>
  <summary>Click to expand demo response</summary>

```json
{
  "schaffrillas": {
    "username": "schaffrillas",
    "display_name": "Schaffrillas",
    "avatar": {
      "exists": true,
      "upscaled": false,
      "url": "https://a.ltrbxd.com/resized/avatar/upload/..."
    },
    "followers_count": 85000,
    "following_count": 12,
    "watched_count": 1500,
    "lists_count": 15,
    "likes_count": 4200
  }
}
```
</details>