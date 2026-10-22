<h2 id="movie_reviews">get_reviews() & get_reviews_by_rating(rating) -> dict</h2>

Fetches member reviews for the movie, with optional star-rating filtering.

```python
from letterboxdpy.movie import Movie

movie_instance = Movie("v-for-vendetta")

# All popular/recent reviews
reviews = movie_instance.get_reviews()

# Filter reviews by a specific rating (e.g. 5.0)
five_star_reviews = movie_instance.get_reviews_by_rating(5.0)

for review_id, review in reviews.items():
    print(f"Author: {review['user']['display_name']} - Rating: {review.get('rating')}")
    print(f"Review: {review['review'][:100]}...\n")
```
