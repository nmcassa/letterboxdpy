<h2 id="get_genre_info">get_genre_info() -> dict</h2>

Extracts genre statistics and film counts for all watched films of the user.

```python
from letterboxdpy.user import User

user_instance = User("nmcassa")
genre_stats = user_instance.get_genre_info()

for genre, count in genre_stats.items():
    print(f"{genre}: {count} films")
```

<details>
  <summary>Click to expand demo response</summary>

```json
{
    "action": 55,
    "adventure": 101,
    "animation": 95,
    "comedy": 188,
    "crime": 22,
    "documentary": 16,
    "drama": 94,
    "family": 109,
    "fantasy": 54,
    "history": 5,
    "horror": 27,
    "music": 9,
    "mystery": 30,
    "romance": 29,
    "science-fiction": 48,
    "thriller": 43,
    "tv-movie": 13,
    "war": 4,
    "western": 5
}
```
</details>