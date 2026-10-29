# User Guide

The `User` class is the primary interface for fetching and analyzing Letterboxd user profiles, watched films, diary entries, social networks, likes, lists, and activity logs.

> [!NOTE]
> Response payloads throughout this guide use sample mock data to demonstrate the returned schema structure without exposing personal accounts.

---

## Initializing a User

You can initialize a `User` instance using their Letterboxd username:

```python
from letterboxdpy.user import User

user = User("bugracoskun")

# Basic Profile Data
print(f"Username: {user.username}")
print(f"Display Name: {user.display_name}")
print(f"Badge: {user.badge}")
print(f"Bio: {user.bio}")
print(f"Location: {user.location}")
print(f"Website: {user.website}")
print(f"Watchlist Length: {user.watchlist_length}")
print(f"Stats: {user.stats}")
```

??? example "Sample `User` Profile Payload (`user.jsonify()`)"

    ```json
    {
      "username": "bugracoskun",
      "url": "https://letterboxd.com/bugracoskun/",
      "id": 1000001,
      "badge": "patron",
      "display_name": "bugra",
      "bio": "Watching movies and writing code.",
      "location": "Istanbul, Turkey",
      "website": "https://bugra.co",
      "watchlist_length": 150,
      "stats": {
        "films": 500,
        "this_year": 25,
        "lists": 10,
        "following": 50,
        "followers": 100
      },
      "favorites": {
        "51940": {
          "slug": "three-colours-red",
          "name": "Three Colours: Red",
          "year": 1994,
          "url": "https://letterboxd.com/film/three-colours-red/"
        },
        "51727": {
          "slug": "once-upon-a-time-in-the-west",
          "name": "Once Upon a Time in the West",
          "year": 1968,
          "url": "https://letterboxd.com/film/once-upon-a-time-in-the-west/"
        },
        "...": "..."
      },
      "avatar": {
        "exists": true,
        "upscaled": true,
        "url": "https://a.ltrbxd.com/resized/avatar/upload/sample_avatar.jpg"
      },
      "backdrop": {
        "url": "https://a.ltrbxd.com/resized/alternative-backdrop/sample_backdrop.jpg",
        "offset": 240
      },
      "recent": {
        "watchlist": {
          "51557": {
            "slug": "constantine",
            "name": "Constantine",
            "year": 2005,
            "url": "https://letterboxd.com/film/constantine/"
          },
          "...": "..."
        },
        "diary": {
          "months": {
            "10": {
              "21": [
                {
                  "name": "Insomnia",
                  "slug": "insomnia"
                }
              ],
              "...": "..."
            }
          }
        }
      }
    }
    ```

---

## Watched Films & Ratings

Fetch all watched films, filter by specific ratings, or extract unrated films:

```python
# 1. Fetch all watched films
films_data = user.get_films()
print(f"Total films: {films_data['count']}")
print(f"Average rating: {films_data['rating_average']}")

# 2. Filter films rated 5.0 stars
five_stars = user.get_films_by_rating(5.0)

# 3. Get watched films without a rating
unrated = user.get_films_not_rated()
```

??? example "Sample `get_films()` Response Payload (Truncated)"

    ```json
    {
      "movies": {
        "companion-2025": {
          "slug": "companion-2025",
          "name": "Companion",
          "year": 2025,
          "url": "https://letterboxd.com/film/companion-2025/",
          "id": "977172",
          "rating": 3.5,
          "liked": true
        },
        "obsession-2025": {
          "slug": "obsession-2025",
          "name": "Obsession",
          "year": 2025,
          "url": "https://letterboxd.com/film/obsession-2025/",
          "id": "1234472",
          "rating": 3.5,
          "liked": false
        },
        "...": "..."
      },
      "count": 500,
      "liked_count": 100,
      "rating_count": 480,
      "liked_percentage": 20.0,
      "rating_percentage": 96.0,
      "rating_average": 3.50
    }
    ```

---

## Diary & Year in Review

Track chronologically logged movies, diary entries, and yearly wrapped summaries:

```python
# Diary entries for a specific year
diary = user.get_diary(year=2024)

# Diary entries for a specific month
october_diary = user.get_diary_month(year=2024, month=10)

# Yearly Wrapped summary statistics
wrapped = user.get_wrapped(year=2024)
print(f"Total logged: {wrapped.get('total_films')}")
```

??? example "Sample `get_diary()` Response Payload (Truncated)"

    ```json
    {
      "entry_count": 24,
      "months": {
        "10": {
          "21": [
            {
              "name": "Insomnia",
              "slug": "insomnia",
              "rating": 4.0,
              "liked": true,
              "rewatch": false
            }
          ],
          "...": "..."
        }
      }
    }
    ```

---

## Social Network (Following & Followers)

Extract the user's community connections with optional pagination and limits:

```python
# Following (users this member follows)
following = user.get_following(page=1, limit=5)
print(f"Following count: {len(following)}")

# Followers (users following this member)
followers = user.get_followers(page=1, limit=5)
print(f"Followers count: {len(followers)}")
```

??? example "Sample `get_following()` Response Payload (Truncated)"

    ```json
    {
      "sample_user_1": {
        "username": "sample_user_1",
        "name": "Sample Cinephile",
        "url": "https://letterboxd.com/sample_user_1/",
        "followers": 150,
        "following": 80,
        "watched": 420,
        "likes": 50
      },
      "sample_critic": {
        "username": "sample_critic",
        "name": "Film Magazine",
        "url": "https://letterboxd.com/sample_critic/",
        "followers": 5000,
        "following": 120,
        "watched": 900,
        "likes": 30
      },
      "...": "..."
    }
    ```

---

## Genre Distribution & User Tags

Analyze user taste profiles and custom tags:

```python
# Genre distribution across watched films
genre_stats = user.get_genre_info()
print(f"Most watched genre: drama ({genre_stats.get('drama')} films)")

# User tags across reviews, lists, and diary entries
user_tags = user.pages.tags.get_user_tags()
```

??? example "Sample `get_genre_info()` Response Payload (Truncated)"

    ```json
    {
      "drama": 200,
      "action": 150,
      "thriller": 120,
      "science-fiction": 90,
      "comedy": 80,
      "crime": 60,
      "...": "..."
    }
    ```

---

## User Lists

Access lists created by the user or fetch a specific list object:

```python
# Get summary of all public lists created by user
lists = user.get_lists()
print(f"Total user lists: {lists['count']}")

# Retrieve a specific List instance directly
user_list = user.get_list("cold-palettes-dark-cities")
print(f"List Title: {user_list.title} ({len(user_list.movies)} films)")
```

---

## API Reference

For full parameter details, return types, and docstrings, see the [User API Reference](../api/user.md).
