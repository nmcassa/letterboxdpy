<h2 id="movie_details">movie_details(movie object)</h2>

```python
from letterboxdpy import movie
movie_instance = movie.Movie("v-for-vendetta")
print(movie.movie_details(movie_instance))
```

<details>
  <summary>Click to expand <code>movie_details</code> method response</summary>

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
        "F\u00fcnfte Babelsberg Film",
        "Warner Bros. Productions",
        "DC Vertigo"
    ],
    "Language": [
        "English"
    ]
}
```
</details>