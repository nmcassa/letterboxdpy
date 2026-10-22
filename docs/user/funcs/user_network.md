<h2 id="user_network">User Network Methods</h2>

Access user social connections, followers, and following lists.

```python
from letterboxdpy.user import User

user_instance = User("nmcassa")

# Get followers (first page)
followers = user_instance.get_followers()

# Get following with pagination
following = user_instance.get_following(page=1, limit=2)
```

Direct module access via `letterboxdpy.pages.user_network`:

```python
from letterboxdpy.pages.user_network import extract_network

# section must be 'followers' or 'following'
data = extract_network("nmcassa", section="followers", page=1, limit=2)
```

**Parameters for `extract_network`:**
- `username` (str): Target Letterboxd username.
- `section` (str): `'followers'` or `'following'`.
- `page` (int, optional): Starting page number. Defaults to 1.
- `limit` (int, optional): Maximum pages to traverse.

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
