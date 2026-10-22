<h2 id="get_lists">get_lists() -> dict</h2>

Fetches all public lists created by the user, including movie count, likes, and comment numbers.

```python
from letterboxdpy.user import User

user_instance = User("nmcassa")

# Get summary of all user lists
lists_data = user_instance.get_lists()
print(f"Total lists: {lists_data['count']}")

# Access a specific list as a List instance
single_list = user_instance.get_list("def-con-movie-list")
print(f"List title: {single_list.title}")

# Get lists liked by the user
liked_lists = user_instance.get_liked_lists()
```

<details>
  <summary>Click to expand demo response</summary>

```json
{
  "lists": {
    "30052453": {
      "title": "DEF CON Movie List",
      "slug": "def-con-movie-list",
      "description": "The DEF CON Hacking Conference's suggested movie list.",
      "url": "https://letterboxd.com/nmcassa/list/def-con-movie-list/",
      "count": 11,
      "likes": 0,
      "comments": 0
    }
  },
  "count": 1,
  "last_page": 1
}
```
</details>