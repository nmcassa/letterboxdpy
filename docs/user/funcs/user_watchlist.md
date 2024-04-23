<h2 id="user_watchlist">user_watchlist(user object)</h2>

```python
from letterboxdpy import user
user_instance = user.User("nmcassa")
watchlist_result = user.user_watchlist(user_instance, {'genre':['action','-drama']})
print(watchlist_result)
```

<details>
  <summary>Click to expand <code>user_watchlist</code> method response</summary>

```json
{
  "available": true,
  "count": 57,
  "data_count": 6,
  "last_page": 1,
  "filters": {
    "genre": [
      "action",
      "-drama"
    ]
  },
  "data": {
    "51397": {
      "name": "From Dusk Till Dawn",
      "slug": "from-dusk-till-dawn",
      "no": 6,
      "page": 1,
      "url": "https://letterboxd.com/films/from-dusk-till-dawn/"
    },...
    "62780": {
      "name": "Mad Max: Fury Road",
      "slug": "mad-max-fury-road",
      "no": 1,
      "page": 1,
      "url": "https://letterboxd.com/films/mad-max-fury-road/"
    }
  }
}
```
</details>