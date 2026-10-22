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
  },
  "ramenfeedgg": {
    "username": "ramenfeedgg",
    "name": "ramenfeedgg",
    "url": "https://letterboxd.com/ramenfeedgg",
    "avatar": {
      "exists": false,
      "upscaled": false,
      "url": "https://s.ltrbxd.com/static/img/avatar80-CTtJ8HSs.png"
    },
    "followers": 7,
    "following": 8,
    "watched": 224,
    "lists": 0,
    "likes": 5
  }
}
```
</details>
