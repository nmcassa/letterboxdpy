# Movie Guide

The `Movie` class fetches metadata, statistics, reviews, cast, crew, external IDs, and recommendations for films on Letterboxd.

---

## Initializing a Movie

You can initialize a `Movie` instance using a Letterboxd slug or external service identifier (TMDB ID or IMDb ID):

```python
from letterboxdpy.movie import Movie

# 1. By slug
movie = Movie("v-for-vendetta")

# 2. By TMDB ID (integer or string)
movie_tmdb = Movie.from_tmdb(752)

# 3. By IMDb ID (string with 'tt' prefix)
movie_imdb = Movie.from_imdb("tt0434409")
```

??? example "Example `Movie` Profile Payload (`movie.jsonify()`)"

    ```json
    {
      "url": "https://letterboxd.com/film/v-for-vendetta/",
      "slug": "v-for-vendetta",
      "id": "51400",
      "title": "V for Vendetta",
      "original_title": null,
      "year": 2005,
      "runtime": 132,
      "rating": 3.84,
      "tmdb_link": "https://www.themoviedb.org/movie/752/",
      "tmdb_id": "752",
      "imdb_link": "https://www.imdb.com/title/tt0434409/maindetails",
      "imdb_id": "tt0434409",
      "poster": "https://a.ltrbxd.com/resized/film-poster/5/1/4/0/0/51400-v-for-vendetta-0-230-0-345-crop.jpg",
      "banner": "https://a.ltrbxd.com/resized/sm/upload/mx/jg/tz/ni/v-for-vendetta-1920-1920-1080-1080-crop-000000.jpg",
      "tagline": "People should not be afraid of their governments. Governments should be afraid of their people.",
      "description": "In a world in which Great Britain has become a fascist state, a masked vigilante known only as 'V' conducts guerrilla warfare against the regime.",
      "trailer": {
        "id": "3ge0navn9E0",
        "link": "https://www.youtube.com/watch?v=3ge0navn9E0",
        "embed_url": "https://www.youtube.com/embed/3ge0navn9E0"
      },
      "genres": [
        {"name": "Action", "slug": "action", "url": "https://letterboxd.com/films/genre/action/"},
        {"name": "Thriller", "slug": "thriller", "url": "https://letterboxd.com/films/genre/thriller/"}
      ],
      "cast": [
        {"name": "Natalie Portman", "role_name": "Evey Hammond", "slug": "natalie-portman"},
        {"name": "Hugo Weaving", "role_name": "V", "slug": "hugo-weaving"}
      ],
      "crew": {
        "director": [{"name": "James McTeigue", "slug": "james-mcteigue"}],
        "writer": [{"name": "Lilly Wachowski", "slug": "lilly-wachowski"}]
      }
    }
    ```

---

## Cast, Crew & Extended Details

Letterboxd exposes both primary details on the film page and in-depth metadata on the sub-details page:

```python
# Access directors, writers, and producers
directors = movie.crew.get("director", [])
for d in directors:
    print(f"Director: {d['name']}")

# Extended details (studios, countries, spoken languages)
extended = movie.get_details_from_details()
print(f"Studios: {extended.get('studios')}")
print(f"Countries: {extended.get('countries')}")
print(f"Languages: {extended.get('languages')}")
```

??? example "Example `get_details_from_details()` Response Payload"

    ```json
    {
      "studios": ["Virtual Studios", "Silver Pictures", "Anarchos Productions"],
      "countries": ["United States", "United Kingdom", "Germany"],
      "languages": ["English"],
      "alternative_titles": ["Vendetta", "O za osvetu", "V de Vingança"]
    }
    ```

---

## Community Stats & Watchers

Extract how many Letterboxd members have watched, liked, or listed the movie:

```python
stats = movie.get_watchers_stats()
print(f"Watchers: {stats.get('watchers')}")
print(f"Fans: {stats.get('fans')}")
print(f"Likes: {stats.get('likes')}")
```

??? example "Example `get_watchers_stats()` Response Payload"

    ```json
    {
      "watchers": 1254300,
      "fans": 84200,
      "likes": 312000,
      "reviews": 45100
    }
    ```

---

## Reviews & Ratings

Read community reviews with optional filtering by star rating:

```python
# Popular reviews listed on the film page
for review in movie.popular_reviews[:3]:
    print(f"- {review['user']['display_name']}: {review['rating']} stars")
    print(f"  \"{review['review']}\"")

# Fetch paginated reviews or filter by exact rating
five_star_reviews = movie.get_reviews_by_rating(5.0)
```

??? example "Example Popular Review Structure"

    ```json
    {
      "user": {
        "username": "zoeyluke",
        "display_name": "zoey luke"
      },
      "link": "https://letterboxd.com/zoeyluke/film/v-for-vendetta/3/",
      "rating": 4.5,
      "review": "A timeless classic with outstanding cinematography and message."
    }
    ```

---

## Similar Movies & Recommendations

Retrieve films that Letterboxd associates with this title based on member viewing habits:

```python
similar = movie.get_similar_movies()
for film_id, item in similar.items():
    print(f"- {item['name']} ({item['year']}) -> {item['url']}")
```

??? example "Example `get_similar_movies()` Response Payload"

    ```json
    {
      "51315": {
        "slug": "equilibrium",
        "name": "Equilibrium",
        "year": 2002,
        "url": "https://letterboxd.com/film/equilibrium/"
      },
      "48210": {
        "slug": "children-of-men",
        "name": "Children of Men",
        "year": 2006,
        "url": "https://letterboxd.com/film/children-of-men/"
      }
    }
    ```

---

## Lists Containing Film

Find public curated lists that include this title:

```python
lists_data = movie.get_lists()
for lst in lists_data.get("lists", []):
    print(f"- {lst['title']} by @{lst['author']}")
```

---

## API Reference

For detailed function definitions, parameters, and return types, see the [Movie API Reference](../api/movie.md).
