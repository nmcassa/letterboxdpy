<h2 id="movie_details">get_details_from_details() -> dict</h2>

Fetches extended movie metadata (studios, countries, languages, alternative titles) from the film's `/details/` subpage.

```python
from letterboxdpy.movie import Movie

movie_instance = Movie("v-for-vendetta")

# Extended details from the /details/ tab
details = movie_instance.get_details_from_details()
print(details)

# Basic details attribute on Movie instance
print(movie_instance.details)
```

<details>
  <summary>Click to expand demo response</summary>

```json
{
    "Country": [
        "Germany",
        "UK",
        "USA"
    ],
    "Studio": [
        "Virtual Studios",
        "Anarchos Productions",
        "Silver Pictures",
        "Warner Bros. Productions",
        "DC Vertigo"
    ],
    "Language": [
        "English"
    ]
}
```
</details>