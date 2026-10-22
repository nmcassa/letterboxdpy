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
