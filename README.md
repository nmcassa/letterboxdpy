# letterboxdpy

[![PyPI version](https://img.shields.io/pypi/v/letterboxdpy?color=blue)](https://pypi.org/project/letterboxdpy/)
[![Python Version](https://img.shields.io/pypi/pyversions/letterboxdpy?color=blue)](https://pypi.org/project/letterboxdpy/)
[![Wheel](https://img.shields.io/pypi/wheel/letterboxdpy?color=blue)](https://pypi.org/project/letterboxdpy/)
[![License](https://img.shields.io/pypi/l/letterboxdpy?color=blue)](https://github.com/nmcassa/letterboxdpy/blob/main/LICENSE)
[![Downloads](https://static.pepy.tech/personalized-badge/letterboxdpy?period=total&units=none&left_color=grey&right_color=blue&left_text=Downloads)](https://pepy.tech/project/letterboxdpy)

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

> [!WARNING]
> Please be aware that installing directly from the GitHub repository might give you access to the most recent features and bug fixes, but it could also include changes that haven't been thoroughly tested and may not be stable for production use.

<h1 id="User">User Object</h1>

[Explore the file](letterboxdpy/user.py) | [Functions Documentation](/docs/user/funcs/)

```python
from letterboxdpy.user import User
user_instance = User("nmcassa")
print(user_instance)
```

<details>
  <summary>Click to expand <code>User</code> object response</summary>
  
```json
{
  "username": "nmcassa",
  "url": "https://letterboxd.com/nmcassa",
  "id": 1500306,
  "is_hq": false,
  "display_name": "nmcassa",
  "bio": null,
  "location": null,
  "website": null,
  "watchlist_length": 76,
  "stats": {
    "films": 702,
    "this_year": 7,
    "lists": 2,
    "following": 8,
    "followers": 8
  },
  "favorites": {
    "51794": {
      "slug": "the-king-of-comedy",
      "name": "The King of Comedy",
      "url": "https://letterboxd.com/film/the-king-of-comedy/",
      "year": 1982,
      "log_url": "https://letterboxd.com/nmcassa/film/the-king-of-comedy/activity/"
    },
    "...": "..."
  },
  "avatar": {
    "exists": true,
    "upscaled": true,
    "url": "https://a.ltrbxd.com/resized/avatar/upload/1/5/0/0/3/0/6/shard/avtr-0-1000-0-1000-crop.jpg"
  },
  "recent": {
    "watchlist": {
      "703077": {
        "id": "703077",
        "slug": "magazine-dreams",
        "name": "Magazine Dreams",
        "year": 2023
      },
      "...": "..."
    },
    "diary": {
      "months": {
        "1": {
          "31": [
            {
              "name": "If I Had Legs I'd Kick You",
              "slug": "if-i-had-legs-id-kick-you"
            }
          ],
          "...": "..."
        }
      }
    }
  }
}
```
</details>

<h1 id="Movie">Movie Object</h1>

[Explore the file](letterboxdpy/movie.py) | [Functions Documentation](/docs/movie/funcs/)

```python
from letterboxdpy.movie import Movie
movie_instance = Movie("v-for-vendetta")
print(movie_instance)
```

<details>
  <summary>Click to expand <code>Movie</code> object response</summary>

```json
{
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
  "description": "In a world in which Great Britain has become a fascist state...",
  "trailer": {
    "id": "3ge0navn9E0",
    "link": "https://www.youtube.com/watch?v=3ge0navn9E0",
    "embed_url": "https://www.youtube.com/embed/3ge0navn9E0"
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
    },
    "..."
  ],
  "genres": [
    {
      "type": "genre",
      "name": "Thriller",
      "slug": "thriller",
      "url": "https://letterboxd.com/films/genre/thriller/"
    },
    "..."
  ],
  "cast": [
    {
      "name": "Natalie Portman",
      "role_name": "Evey Hammond",
      "slug": "natalie-portman",
      "url": "https://letterboxd.com/actor/natalie-portman/"
    },
    "..."
  ],
  "crew": {
    "director": [
      {
        "name": "James McTeigue",
        "slug": "james-mcteigue",
        "url": "https://letterboxd.com/director/james-mcteigue/"
      }
    ],
    "...": "..."
  },
  "popular_reviews": [
    {
      "user": {
        "username": "zoeyluke",
        "display_name": "zoey luke"
      },
      "link": "https://letterboxd.com/zoeyluke/film/v-for-vendetta/3/",
      "rating": 4.5,
      "review": "I love natalie Portman and I hate the government"
    },
    "...": "..."
  ]
}
```
</details>

<h1 id="Search">Search Object</h1>

[Explore the file](letterboxdpy/search.py) | [Functions Documentation](/docs/search/funcs/)

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
  "end_page": 1,
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
      "poster": "https://s.ltrbxd.com/static/img/empty-poster-70-BSf-Pjrh.png",
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

<h1 id="List">List Object</h1>

[Explore the file](letterboxdpy/list.py)

```python
from letterboxdpy.list import List
list_instance = List("nmcassa", "movies-to-watch-with-priscilla-park")
print(list_instance)
```

<details>
  <summary>Click to expand <code>List</code> object response</summary>

```json
{
  "username": "nmcassa",
  "slug": "movies-to-watch-with-priscilla-park",
  "_movies": {
    "240344": {
      "slug": "la-la-land",
      "name": "La La Land",
      "year": 2016,
      "url": "https://letterboxd.com/film/la-la-land/"
    },
    "...": "..."
  },
  "url": "https://letterboxd.com/nmcassa/list/movies-to-watch-with-priscilla-park",
  "title": "Movies to Watch with Priscilla Park",
  "author": "nmcassa",
  "description": null,
  "date_created": "2024-05-18T16:44:57.013000Z",
  "date_updated": "2024-05-20T14:58:06.486000Z",
  "tags": [],
  "count": 19,
  "list_id": "46710824"
}
```
</details>

<h1 id="Members">Members Object</h1>

[Explore the file](letterboxdpy/members.py) | [Functions Documentation](/docs/members/funcs/)

```python
from letterboxdpy.members import top_users
print(top_users(max=5))
```

<details>
  <summary>Click to expand <code>Members</code> object response</summary>

```json
[
  "schaffrillas",
  "kurstboy",
  "demiadejuyigbe",
  "zoerosebryant",
  "jaragon23"
]
```
</details>

<h1 id="Films">Films Object</h1>

[Explore the file](letterboxdpy/films.py) | [Functions Documentation](/docs/films/funcs/)

```python
from letterboxdpy.films import Films
films_instance = Films("https://letterboxd.com/films/popular/", max=3)
print(films_instance.movies)
```

<details>
  <summary>Click to expand <code>Films</code> object response</summary>

```json
{
  "1197499": {
    "slug": "marty-supreme",
    "name": "Marty Supreme",
    "rating": 4.21,
    "url": "https://letterboxd.com/film/marty-supreme/"
  },
  "772232": {
    "slug": "hamnet",
    "name": "Hamnet",
    "rating": 4.22,
    "url": "https://letterboxd.com/film/hamnet/"
  },
  "1116600": {
    "slug": "sinners-2025",
    "name": "Sinners",
    "rating": 4.11,
    "url": "https://letterboxd.com/film/sinners-2025/"
  }
}
```
</details>

<h1 id="Watchlist">Watchlist Object</h1>

[Explore the file](letterboxdpy/watchlist.py)

```python
from letterboxdpy.watchlist import Watchlist
watchlist = Watchlist("nmcassa")
# movies loaded when accessed
print(watchlist)
```

<details>
  <summary>Click to expand <code>Watchlist</code> object response</summary>

```json
{
  "username": "nmcassa",
  "url": "https://letterboxd.com/nmcassa/watchlist",
  "count": 134,
  "movies": {
    "51315": {
      "slug": "videodrome",
      "name": "Videodrome",
      "year": 1983,
      "url": "https://letterboxd.com/film/videodrome/"
    },
    "...": "..."
  }
}
```
</details>

<h1 id="Authentication">Authentication & Sessions</h1>

[Explore the file](letterboxdpy/auth.py)

The `UserSession` module unlocks account-specific features like **profile customization** and **settings management**. It handles login securely and persists your session, so you don't have to sign in every time.

```python
from letterboxdpy.auth import UserSession

# Logs in if no session exists, or loads the saved session automatically
session = UserSession.ensure()

# 2. Programmatic login
# session = UserSession.login("username", "password")

# 3. Manual load from custom path
# session = UserSession.load(Path(".cookie/session.json"))

print(f"Authenticated as: {session.username}")
```

<h1 id="Settings">User Settings</h1>

[Explore the file](letterboxdpy/account/settings.py)

The `UserSettings` module allows reading and updating user profile and notification settings. **Requires an authenticated session.**

```python
from letterboxdpy.account.settings import UserSettings

settings = UserSettings(session)

# Get current profile data
profile = settings.get_profile()
print(f"Current Bio: {profile['bio']}")

# Update specific profile fields
settings.update_profile({
    "location": "New York, USA",
    "website": "https://example.com",
    "bio": "Just another movie lover."
})

# Manage notifications
notifs = settings.get_notifications()
settings.update_notifications({"emailEditorial": True, "pushFollowers": False})
```

<h1 id="Examples">Examples</h1>

Example scripts demonstrating various features are available in the [`examples/`](examples/) directory.

See [`examples/README.md`](examples/README.md) for detailed usage instructions.

<h1 id="Testing">Testing</h1>

You may test the plugin by using the built-in `unittest` package through the CLI:

```zsh
python -m unittest <TEST_FILE_LINK>
```

**Example**
```zsh
python -m unittest tests/test_movie.py
```

## Stargazers over time
[![Stargazers over time](https://starchart.cc/nmcassa/letterboxdpy.svg?background=%2300000000&axis=%23848D97&line=%23238636)](https://starchart.cc/nmcassa/letterboxdpy)