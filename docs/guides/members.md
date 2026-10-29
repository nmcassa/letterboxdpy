# Members Guide

The `Members` class extracts community member data, popular profiles, and leaderboards from Letterboxd.

---

## Quick Example

```python
from letterboxdpy.members import Members

# Fetch top 5 popular members of the year
members = Members(max=5)
print(members.members)
```

??? example "Example `Members` Output"

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

You can pass custom Letterboxd member catalog URLs:

```python
# All-time popular members
all_time = Members("https://letterboxd.com/members/popular/", max=20)
for username in all_time.members:
    print(f"- {username}")
```

---

## API Reference

For detailed function definitions, see the [Members API Reference](../api/members.md).

