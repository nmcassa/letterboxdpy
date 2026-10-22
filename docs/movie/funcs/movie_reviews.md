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
  "available": false,
  "count": 0,
  "reviews": []
}
```
</details>

> [!NOTE]
> Movie review scraping is not implemented yet. `get_reviews()` and
> `get_reviews_by_rating()` currently return the stub response shown above.
> Use `popular_reviews` for review data scraped from the film page.
