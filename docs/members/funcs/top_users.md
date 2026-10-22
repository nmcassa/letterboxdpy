<h2 id="top_users">top_users(max: int = 100) -> list</h2>

Fetches usernames of the most popular members from Letterboxd's popular members page.

```python
from letterboxdpy.members import top_users, Members

# Using helper function
popular = top_users(max=5)
print(popular)
# Output: ['schaffrillas', 'kurstboy', 'demiadejuyigbe', 'zoerosebryant', 'jaragon23']

# Or using the Members class directly
members_instance = Members(max=10)
print(members_instance.members)
```

**Parameters:**
- `max` (int, optional): Maximum number of member usernames to return. Defaults to 100.

**Returns:**
- `list[str]`: List of usernames.
