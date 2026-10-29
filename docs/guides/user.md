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
              "id": "12890",
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

## Reviews

Fetch all written reviews by the user across all films. Each review includes the movie info, log type, rating (parsed from Letterboxd's SVG star glyphs), review text, spoiler flag, and ISO 8601 date:

```python
reviews_data = user.get_reviews()
print(f"Total reviews: {reviews_data['count']}")

for log_id, review in reviews_data["reviews"].items():
    movie = review["movie"]
    rating = review["rating"]  # float (0.5–5.0) or None if unrated
    print(f"{movie['name']} ({movie['release']}) — {rating}★")
    print(f"  {review['review']['content'][:80]}")
```

??? example "Sample `get_reviews()` Response Payload (Truncated)"

    ```json
    {
      "reviews": {
        "987654321": {
          "movie": {
            "name": "The Prestige",
            "slug": "the-prestige",
            "id": "60744",
            "release": 2006,
            "link": "https://letterboxd.com/film/the-prestige/"
          },
          "type": "Watched",
          "no": 0,
          "link": "https://letterboxd.com/bugracoskun/film/the-prestige/",
          "rating": 4.5,
          "review": {
            "content": "One of Nolan's best. The final reveal lands every time.",
            "spoiler": false
          },
          "date": "2024-10-21T00:00:00.000000Z",
          "page": 1
        },
        "...": "..."
      },
      "count": 42,
      "last_page": 4
    }
    ```

> [!NOTE]
> Ratings are parsed from Letterboxd's SVG star glyph elements (`aria-label="★★★★½"`). Both the current SVG format and the legacy `rated-X` class format are supported, so ratings are always populated when present.

---

## Activity

Fetch recent activity for the user or their followed accounts. Each entry includes a unique activity ID, ISO 8601 timestamp, a direct permalink (`url`), and a typed content payload:

```python
# Own recent activity
activity = user.get_activity()
print(f"Total activities: {activity['metadata']['total_activities']}")

for act_id, entry in activity["activities"].items():
    print(f"[{entry['activity_type']}] {entry['date']}")
    print(f"  {entry['content'].get('description', '')}")
    print(f"  {entry['url']}")

# Activity feed from followed accounts
following_activity = user.get_activity_following()
```

??? example "Sample `get_activity()` Response Payload (Truncated)"

    ```json
    {
      "metadata": {
        "export_timestamp": "2024-10-29T18:00:00.000000Z",
        "source_url": "https://letterboxd.com/ajax/activity-pagination/bugracoskun/",
        "total_activities": 15
      },
      "activities": {
        "13321312465": {
          "activity_type": "review",
          "date": "2024-10-26T02:33:21.855000Z",
          "url": "https://letterboxd.com/bugracoskun/film/the-prestige/",
          "content": {
            "action": "watched",
            "description": "bugracoskun watched The Prestige",
            "movie": {
              "title": "The Prestige",
              "year": 2006,
              "slug": "the-prestige",
              "url": "https://letterboxd.com/film/the-prestige/"
            },
            "review": {
              "content": "One of Nolan's best.",
              "contains_spoilers": false
            }
          }
        },
        "13321312400": {
          "activity_type": "basic",
          "date": "2024-10-25T14:10:00.000000Z",
          "url": "https://letterboxd.com/film/inception/",
          "content": {
            "action": "watched",
            "description": "bugracoskun watched Inception",
            "movie": {
              "title": "Inception",
              "year": 2010,
              "slug": "inception",
              "url": "https://letterboxd.com/film/inception/"
            }
          }
        },
        "...": "..."
      }
    }
    ```

> [!NOTE]
> Activity types are `review` (watched + wrote a review), `basic` (watched without a review), and `newlist` (created a list). The `url` field is a direct permalink to the film page or list — useful for deep-linking directly to the relevant content.

---

## API Reference

For full parameter details, return types, and docstrings, see the [User API Reference](../api/user.md).
