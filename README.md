# letterboxdpy

[![PyPI version](https://badge.fury.io/py/letterboxdpy.svg)](https://badge.fury.io/py/letterboxdpy)
[![Downloads](https://static.pepy.tech/personalized-badge/letterboxdpy?period=total&units=none&left_color=grey&right_color=blue&left_text=Downloads)](https://pepy.tech/project/letterboxdpy)
![format](https://img.shields.io/pypi/format/letterboxdpy)

## Installation

### From PyPI

You can easily install the stable version of `letterboxdpy` from PyPI using pip:

```bash
pip install letterboxdpy
```

### From GitHub Repository

Alternatively, if you wish to access the latest (potentially unstable) version directly from the GitHub repository, you can execute the following command:

```bash
pip install git+https://github.com/nmcassa/letterboxdpy.git
```

**Note:** Please be aware that installing directly from the GitHub repository might give you access to the most recent features and bug fixes, but it could also include changes that haven't been thoroughly tested and may not be stable for production use.

# Directory
  - [User Object](#User)
     - **props**: scraper, username, url, avatar, recent, id, is_hq, display_name, bio, location, website, watchlist_length, stats, favorites
    - **funcs**: [user_films](/docs/user/funcs/user_films.md), [user_following](/docs/user/funcs/user_following.md), [user_followers](/docs/user/funcs/user_followers.md), [user_genre_info](/docs/user/funcs/user_genre_info.md), [user_reviews](/docs/user/funcs/user_reviews.md), [user_diary](/docs/user/funcs/user_diary.md), [user_wrapped](/docs/user/funcs/user_wrapped.md), [user_activity](/docs/user/funcs/user_activity.md), [user_lists](/docs/user/funcs/user_lists.md), [user_watchlist](/docs/user/funcs/user_watchlist.md), [user_tags](/docs/user/funcs/user_tags.md)
  - [Movie Object](#Movie)
    - **props**: scraper, url, slug, banner, trailer, cast, crew, details, alternative_titles, genres, rating, year, poster, tagline, description, popular_reviews, letterboxd_id, title, original_title, runtime, tmdb_link, imdb_link
    - **funcs**: [movie_details](/docs/movie/funcs/movie_details.md), [movie_watchers](/docs/movie/funcs/movie_watchers.md)
  - [List Object](#List)
    - **props**: scraper, url, slug, username, list_type, items_per_page, title, author, date_created, date_updated, description, tags, movies, count
  - [Search Object](#Search):
  - [Members Object](#Members)


<h1 id="User">User Object</h1>

```python
from letterboxdpy.user import User
user_instance = User("nmcassa")
print(user_instance)
```

<details>
  <summary>Click to expand <code>User</code> object response</summary>
  
```json
{
  "scraper": {...},
  "username": "nmcassa",
  "url": "https://letterboxd.com/nmcassa",
  "id": "1500306",
  "is_hq": false,
  "display_name": "nmcassa",
  "bio": null,
  "location": null,
  "website": null,
  "watchlist_length": 64,
  "stats": {
    "films": 560,
    "this_year": 37,
    "list": 1,
    "following": 10,
    "followers": 8
  },
  "favorites": {
    "95113": {
      "slug": "the-grand-budapest-hotel",
      "name": "The Grand Budapest Hotel"
    },...
  },
  "avatar": {
    "exists": true,
    "upscaled": true,
    "url": "https://a.ltrbxd.com/resized/avatar/upload/1/5/0/0/3/0/6/shard/avtr-0-1000-0-1000-crop.jpg"
  },
  "recent": {
    "watchlist": {
      "7023": {
        "name": "The Man Who Stole the Sun",
        "slug": "the-man-who-stole-the-sun"
      },...
    },
    "diary": {
      "months": {
        "4": [
          [
            "16",
            "Civil War"
          ],...
        ],
        "3": [
          [
            "30",
            "Dune"
          ],...
        ]
      }
    }
  }
}
```
</details>

<h1 id="Movie">Movie Object</h1>

```python
from letterboxdpy.movie import Movie
movie_instance = Movie("v-for-vendetta")
print(movie_instance)
```

<details>
  <summary>Click to expand <code>Movie</code> object response</summary>

```json
{
  "scraper": {...},
  "url": "https://letterboxd.com/film/v-for-vendetta",
  "slug": "v-for-vendetta",
  "letterboxd_id": 51400,
  "title": "V for Vendetta",
  "original_title": null,
  "runtime": 132,
  "rating": 3.84,
  "year": 2005,
  "tmdb_link": "https://www.themoviedb.org/movie/752/",
  "imdb_link": "http://www.imdb.com/title/tt0434409/maindetails",
  "poster": "https://a.ltrbxd.com/resized/film-poster/5/1/4/0/0/51400-v-for-vendetta-0-230-0-345-crop.jpg",
  "banner": "https://a.ltrbxd.com/resized/sm/upload/mx/jg/tz/ni/v-for-vendetta-1920-1920-1080-1080-crop-000000.jpg",
  "tagline": "People should not be afraid of their governments. Governments should be afraid of their people.",
  "description": "In a world in which Great Britain has become a fascist state, a masked vigilante known only as \u201cV\u201d conducts guerrilla warfare against the oppressive British government. When V rescues a young woman from the secret police, he finds in her an ally with whom he can continue his fight to free the people of Britain.",
  "trailer": {
    "id": "V5VGq23aZ-g",
    "link": "https://www.youtube.com/watch?v=V5VGq23aZ-g",
    "embed_url": "https://www.youtube.com/embed/V5VGq23aZ-g"
  },
  "alternative_titles": [
    "Vendetta \u00fc\u00e7\u00fcn V",
    "O za osvetu",...
  ],
  "details": [
    {
      "type": "studio",
      "name": "Virtual Studios",
      "slug": "virtual-studios",
      "url": "https://letterboxd.com/studio/virtual-studios/"
    },...
  ],
  "genres": [
    {
      "type": "genre",
      "name": "Thriller",
      "slug": "thriller",
      "url": "https://letterboxd.com/films/genre/thriller/"
    },...
  ],
  "cast": [
    {
      "name": "Natalie Portman",
      "role_name": "Evey Hammond",
      "slug": "natalie-portman",
      "url": "https://letterboxd.com/actor/natalie-portman/"
    },...
  ],
  "crew": {
    "director": [
      {
        "name": "James McTeigue",
        "slug": "james-mcteigue",
        "url": "https://letterboxd.com/director/james-mcteigue/"
      }
    ],
    "producer": [
      {
        "name": "Grant Hill",
        "slug": "grant-hill",
        "url": "https://letterboxd.com/producer/grant-hill/"
      },...
    ],...
  },
  "popular_reviews": [
    {
      "reviewer": "zoey luke",
      "rating": " \u2605\u2605\u2605\u2605\u00bd ",
      "review": "I love natalie Portman and I hate the government"
    },...
  ]
}
}
```
</details>


<h1 id="List">List Object</h1>

```python
from letterboxdpy.list import List
list_instance = List("hepburnluv", "classic-movies-for-beginners")
print(list_instance)
```

<details>
  <summary>Click to expand <code>List</code> object response</summary>

```json
{
  "scraper": {...},
  "url": "https://letterboxd.com/hepburnluv/list/classic-movies-for-beginners",
  "slug": "classic-movies-for-beginners",
  "username": "hepburnluv",
  "list_type": "list",
  "items_per_page": 60,
  "title": "classic movies for beginners.",
  "description": "old hollywood classic movies for you who wanna start watching. \u02d6\u207a\u2027\u208a\u02da \u2661 \u02da\u208a\u2027\u207a\u02d6. \u0741\u208a \u22b9 . \u0741(from easiest to hardest to watch) (these are my personal recommendations only) thank you guys for all the comments and likes <3",
  "movies": [
    [
      "The Wizard of Oz",
      "the-wizard-of-oz-1939"
    ],
    [
      "Roman Holiday",
      "roman-holiday"
    ],...
  ],
  "count": 66
}
```
</details>

<h1 id="Search">Search Object</h1>

```python
from letterboxdpy.search import Search
search_instance = Search("V for Vendetta", 'films')
print(search_instance.get_results(max=5))
```

<details>
  <summary>Click to expand <code>Search</code> object response</summary>

```json
{
  "available": true,
  "query": "V%20for%20Vendetta",
  "filter": "films",
  "end_page": 13,
  "count": 5,
  "results": [
    {
      "no": 1,
      "page": 1,
      "type": "film",
      "slug": "v-for-vendetta",
      "name": "V for Vendetta",
      "year": 2005,
      "url": "https://letterboxd.com/film/v-for-vendetta/",
      "poster": null,
      "directors": [
        {
          "name": "James McTeigue",
          "slug": "james-mcteigue",
          "url": "https://letterboxd.com/director/james-mcteigue/"
        }
      ]
    },
    {
      "no": 2,
      "page": 1,
      "type": "film",
      "slug": "lady-vengeance",
      "name": "Lady Vengeance",
      "year": 2005,
      "url": "https://letterboxd.com/film/lady-vengeance/",
      "poster": null,
      "directors": [
        {
          "name": "Park Chan-wook",
          "slug": "park-chan-wook",
          "url": "https://letterboxd.com/director/park-chan-wook/"
        }
      ]
    },...
  ]
}
```
</details>


<h1 id="Search">Members Object</h1>

[To be documented.](https://github.com/search?q=repo:nmcassa/letterboxdpy+Members)

## Stargazers over time
[![Stargazers over time](https://starchart.cc/nmcassa/letterboxdpy.svg?background=%2300000000&axis=%23848D97&line=%23238636)](https://starchart.cc/nmcassa/letterboxdpy)