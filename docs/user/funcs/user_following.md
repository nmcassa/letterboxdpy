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
  "rosertpp": {
    "username": "rosertpp",
    "name": "rosertpp",
    "url": "https://letterboxd.com/rosertpp",
    "avatar": {
      "exists": true,
      "upscaled": true,
      "url": "https://a.ltrbxd.com/resized/avatar/upload/1/5/9/0/6/5/5/2/shard/avtr-0-1000-0-1000-crop.jpg"
    },
    "followers": 6,
    "following": 4,
    "watched": 189,
    "lists": 1,
    "likes": 67
  },
  "moldylungs": {
    "username": "moldylungs",
    "name": "2d",
    "url": "https://letterboxd.com/moldylungs",
    "avatar": {
      "exists": true,
      "upscaled": true,
      "url": "https://a.ltrbxd.com/resized/avatar/upload/3/9/9/7/0/1/7/shard/avtr-0-1000-0-1000-crop.jpg"
    },
    "followers": 14,
    "following": 18,
    "watched": 180,
    "lists": 0,
    "likes": 144
  }
}
```
</details>