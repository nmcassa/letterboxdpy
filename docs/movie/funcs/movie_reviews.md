<h2 id="movie_reviews">get_reviews() & get_reviews_by_rating(rating) -> dict</h2>

Fetches member reviews for the movie, with optional star-rating filtering.

```python
from letterboxdpy.movie import Movie

movie_instance = Movie("v-for-vendetta")

# All reviews via MovieReviews
reviews = movie_instance.get_reviews()

# Filter reviews by a specific rating (e.g. 5.0)
five_star_reviews = movie_instance.get_reviews_by_rating(5.0)

# Or access curated popular reviews directly from the movie page
for review in movie_instance.popular_reviews:
    print(f"Author: {review['user']['display_name']} - Rating: {review.get('rating')}")
    print(f"Review: {review['review'][:100]}...\n")
```

<details>
  <summary>Click to expand demo response</summary>

```json
{
  "available": true,
  "count": 2,
  "reviews": [
    {
      "user": {
        "username": "filmcritic",
        "display_name": "Film Critic"
      },
      "link": "https://letterboxd.com/filmcritic/film/v-for-vendetta/",
      "rating": 4.5,
      "review": "A timeless dystopian classic featuring incredible performances."
    },
    {
      "user": {
        "username": "cinephile99",
        "display_name": "Alex Vance"
      },
      "link": "https://letterboxd.com/cinephile99/film/v-for-vendetta/",
      "rating": 5.0,
      "review": "Hugo Weaving's voice work alone elevates this graphic novel adaptation into masterclass territory."
    }
  ]
}
```
</details>
