<h2 id="get_followers">get_followers(page=1, limit=None) -> dict</h2>

Fetches a dictionary of users following the given account, including social metrics and avatars.

```python
from letterboxdpy.user import User

user_instance = User("nmcassa")

# Fetch first page of followers
followers = user_instance.get_followers()
print(f"Followers on page 1: {len(followers)}")

# Fetch specific page or limit results
followers_p2 = user_instance.get_followers(page=2, limit=50)
```

**Parameters:**
- `page` (int, optional): Page number to start fetching from. Defaults to 1.
- `limit` (int, optional): Maximum number of pages to fetch.

<details>
  <summary>Click to expand demo response</summary>

```json
{
  "ppark": {
    "username": "ppark",
    "display_name": "Priscilla Park",
    "avatar": {
      "exists": true,
      "upscaled": false,
      "url": "https://a.ltrbxd.com/resized/avatar/upload/..."
    },
    "followers_count": 42,
    "following_count": 35,
    "watched_count": 420,
    "lists_count": 3,
    "likes_count": 120
  }
}
```
</details>