# Members Guide

The `Members` class extracts community member data, popular profiles, and leaderboards from Letterboxd.

---

## Quick Example

By default, initializing `Members()` fetches the most popular members of the current year:

```python
from letterboxdpy.members import Members

# Fetch top 5 popular members of the year
members = Members(max=5)

for index, username in enumerate(members.members, start=1):
    print(f"{index}. @{username} (https://letterboxd.com/{username})")
```

??? example "Example `Members` Output (`members.members`)"

    ```json
    [
      "schaffrillas",
      "kurstboy",
      "demiadejuyigbe",
      "zoerosebryant",
      "jaragon23"
    ]
    ```

---

## Custom Member Catalogs

You can pass custom Letterboxd member catalog URLs to scrape all-time popular profiles, monthly rankings, or headquarters staff:

```python
# 1. All-time popular members
all_time = Members("https://letterboxd.com/members/popular/", max=10)

# 2. Popular this week
this_week = Members("https://letterboxd.com/members/popular/this/week/", max=10)

# 3. Letterboxd HQ staff members
hq_staff = Members("https://letterboxd.com/members/popular/hq/", max=10)
```

---

## Combining `Members` with `User`

Iterate through popular members to extract detailed stats for each profile:

```python
from letterboxdpy.members import Members
from letterboxdpy.user import User

top_members = Members(max=3)

for username in top_members.members:
    profile = User(username)
    print(f"@{profile.username} - Watched: {profile.stats.get('films')} films | Followers: {profile.stats.get('followers')}")
```

---

## API Reference

For detailed function definitions, see the [Members API Reference](../api/members.md).
