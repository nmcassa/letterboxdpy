# User Guide

The `User` class is the primary interface for inspecting Letterboxd user profiles, watched films, diary logs, ratings, and social networks.

---

## Quick Example

```python
from letterboxdpy.user import User

user = User("nmcassa")

# Profile attributes
print(f"User ID: {user.id}")
print(f"Display Name: {user.display_name}")
print(f"Bio: {user.bio}")
print(f"Total Watchlist Films: {user.watchlist_length}")

# User stats
print(f"Stats: {user.stats}")
```

??? example "Example `User` Payload Structure"

    ```json
    {
      "username": "nmcassa",
      "url": "https://letterboxd.com/nmcassa",
      "id": 1500306,
      "badge": "member",
      "display_name": "nmcassa",
      "bio": null,
      "location": null,
      "website": null,
      "watchlist_length": 76,
      "stats": {
        "films": 702,
        "this_year": 7,
        "lists": 2,
        "following": 8,
        "followers": 8
      },
      "favorites": {
        "51794": {
          "slug": "the-king-of-comedy",
          "name": "The King of Comedy",
          "url": "https://letterboxd.com/film/the-king-of-comedy/",
          "year": 1982
        }
      }
    }
    ```

---

## Profile Data Extraction

### Watched Films & Ratings

Fetch all watched films, ratings, and summary statistics:

```python
films_data = user.get_films()
print(f"Total watched: {films_data['count']}")
print(f"Liked films: {films_data['liked_count']}")
print(f"Average rating: {films_data['rating_average']}")
```

??? example "Example `get_films()` Payload"

    ```json
    {
      "movies": {
        "civil-war-2024": {
          "name": "Civil War",
          "id": "834656",
          "rating": 1.5,
          "liked": false
        },
        "monkey-man": {
          "name": "Monkey Man",
          "id": "488751",
          "rating": 4.5,
          "liked": true
        }
      },
      "count": 560,
      "liked_count": 80,
      "rating_count": 518,
      "liked_percentage": 14.29,
      "rating_percentage": 92.5,
      "rating_average": 6.47
    }
    ```

### Diary Logs

```python
# Diary entries for a specific year
diary = user.get_diary(year=2024)
```

??? example "Example `get_diary()` Payload"

    ```json
    {
      "entry_count": 24,
      "months": {
        "1": {
          "15": [
            {
              "name": "Poor Things",
              "slug": "poor-things-2023",
              "rating": 4.5,
              "liked": true,
              "rewatch": false
            }
          ]
        }
      }
    }
    ```

### Social Network (Following & Followers)

```python
following = user.get_following()
followers = user.get_followers()
```

??? example "Example `get_following()` Payload"

    ```json
    {
      "count": 8,
      "users": {
        "schaffrillas": {
          "display_name": "James Schaffrillas",
          "url": "https://letterboxd.com/schaffrillas/"
        }
      }
    }
    ```

### Yearly Wrapped Summary

```python
wrapped = user.get_wrapped(year=2024)
```

---

## API Reference

For full parameter signatures, type definitions, and docstrings, see the [User API Reference](../api/user.md).
