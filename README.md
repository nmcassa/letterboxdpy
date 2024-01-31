# letterboxdpy

[![PyPI version](https://badge.fury.io/py/letterboxdpy.svg)](https://badge.fury.io/py/letterboxdpy)
[![Downloads](https://static.pepy.tech/personalized-badge/letterboxdpy?period=total&units=none&left_color=grey&right_color=blue&left_text=Downloads)](https://pepy.tech/project/letterboxdpy)
![format](https://img.shields.io/pypi/format/letterboxdpy)

## Installation

```
pip install letterboxdpy
```

# Directory
 - [User Objects](#User)
    - [user_genre_info](#user_genre_info)
    - [user_following & user_followers](#user_following)
    - [user_films](#user_films)
    - [user_reviews](#user_reviews)
    - [user_diary](#user_diary)
    - [user_diary_page](#user_diary_page) (todo)
    - [user_wrapped](#user_wrapped)
 - [Members](#Members) (todo)
    - [top_users](#top_users) (todo)
 - [Movie Objects](#Movie)
    - [movie_details](#movie_details)
    - [movie_description](#movie_description)
    - [movie_popular_reviews](#movie_popular_reviews)
    - [movie_tmdb_link](#movie_tmdb_link)
    - [movie_watchers](#movie_watchers) (todo)
    - [movie_poster](#movie_poster) (todo)
 - [List Objects](#List)
    - [list_tags](#list_tags)

<h1 id="User">User Objects</h1>

```python
from letterboxdpy import user
nick = user.User("nmcassa")
print(nick)
```

<details>
  <summary>Click to expand User object response</summary>
  
```json
{
    "username": "nmcassa",
    "watchlist_length": "72",
    "favorites": [
        [
            "The Grand Budapest Hotel",
            "/film/the-grand-budapest-hotel/"
        ],
        [
            "The King of Comedy",
            "/film/the-king-of-comedy/"
        ],
        [
            "The Alpinist",
            "/film/the-alpinist/"
        ],
        [
            "The Graduate",
            "/film/the-graduate/"
        ]
    ],
    "stats": {
        "Films": "372",
        "This year": "97",
        "List": "1",
        "Following": "7",
        "Followers": "6"
    }
}
```
</details>

<h2 id="user_genre_info">user_genre_info(user object)</h2>

```python
from letterboxdpy import user
nick = user.User("nmcassa")
print(user.user_genre_info(nick))
```

<details>
  <summary>Click to expand user_genre_info method response</summary>

```json
{
    "action":55,
    "adventure":101,
    "animation":95,
    "comedy":188,
    "crime":22,
    "documentary":16,
    "drama":94,
    "family":109,
    "fantasy":54,
    "history":5,
    "horror":27,
    "music":9,
    "mystery":30,
    "romance":29,
    "science-fiction":48,
    "thriller":43,
    "tv-movie":13,
    "war":4,
    "western":5
}
```
</details>

<h2 id="user_following">user_following(user object) / user_followers(user object)</h2>

```python
from letterboxdpy import user
nick = user.User("nmcassa")
print(user.user_following(nick))
print(user.user_followers(nick))
```

<details>
  <summary>Click to expand user_following & user_followers methods response</summary>

```json
{
    "ppark": {
        "display_name": "ppark"
    },
    "ryanshubert": {
        "display_name": "ryanshubert"
    },
    "crescendohouse": {
        "display_name": "Crescendo House"
    },...
}
   "ppark": {
        "display_name": "ppark"
    },
    "joacogarcia2023": {
        "display_name": "joacogarcia2023"
    },
    "ryanshubert": {
        "display_name": "ryanshubert"
    },...
}
```
</details>

<h2 id="user_films">user_films(user object)</h2>

```python
from letterboxdpy import user
nick = user.User("nmcassa")
print(user.user_films(nick))
```

<details>
  <summary>Click to expand user_films_watched method response</summary>

```json
{
    "movies": {
        "godzilla-minus-one": {
            "name": "Godzilla Minus One",
            "id": "845706",
            "rating": 10,
            "liked": true
        },
        "flcl": {
            "name": "FLCL",
            "id": "284640",
            "rating": null,
            "liked": true
        },...
    },
    "count": 528,
    "liked_count": 73,
    "rating_count": 493,
    "rating_average": 6.43,
    "rating_percentage": 93.37,
    "liked_percentage": 13.83
}
```
</details>

<h2 id="user_reviews">user_reviews(user object)</h2>

```python
from letterboxdpy import user
nick = user.User("nmcassa")
print(user.user_reviews(nick))
```

<details>
  <summary>Click to expand user_reviews method response</summary>

```json
{
    "reviews": {
        "495592379": {
            "movie": {
                "name": "Poor Things",
                "slug": "poor-things-2023",
                "id": "710352",
                "release": 2023,
                "link": "ltrbxd.com/film/poor-things-2023/"
            },
            "type": "Watched",
            "no": 0,
            "link": "ltrbxd.com/nmcassa/film/poor-things-2023/",
            "rating": 6,
            "review": {
                "content": "It looks like AI art and weird movie",
                "spoiler": false
            },
            "date": {
                "year": 2023,
                "month": 12,
                "day": 26
            },
            "page": 1
        },
        "152420824": {
            "movie": {
                "name": "I'm Thinking of Ending Things",
                "slug": "im-thinking-of-ending-things",
                "id": "430806",
                "release": 2020,
                "link": "ltrbxd.com/film/im-thinking-of-ending-things/"
            },
            "type": "Watched",
            "no": 0,
            "link": "ltrbxd.com/nmcassa/film/im-thinking-of-ending-things/",
            "rating": 8,
            "review": {
                "content": "yeah i dont get it",
                "spoiler": false
            },
            "date": {
                "year": 2021,
                "month": 2,
                "day": 14
            },
            "page": 1
        }
    },
    "count": 7,
    "last_page": 1
}
```
</details>

<h2 id="user_diary">user_diary(user object)</h2>

```python
from letterboxdpy import user
nick = user.User("nmcassa")
print(user.user_diary(nick))
```

<details>
  <summary>Click to expand user_diary method response</summary>

```json
{
    "entrys": {
        "513520182": {
            "name": "Black Swan",
            "slug": "black-swan",
            "id": "20956",
            "release": 2010,
            "runtime": 108,
            "rewatched": false,
            "rating": 9,
            "liked": true,
            "reviewed": false,
            "date": {
                "year": 2024,
                "month": 1,
                "day": 15
            },
            "page": 1
        },...
        ...},
        "129707465": {
            "name": "mid90s",
            "slug": "mid90s",
            "id": "370451",
            "release": 2018,
            "runtime": 86,
            "rewatched": false,
            "rating": 8,
            "liked": false,
            "reviewed": false,
            "date": {
                "year": 2020,
                "month": 10,
                "day": 20
            },
            "page": 7
        }
    },
    "count": 337,
    "last_page": 7
}
```
</details>

<h2 id="user_wrapped">user_wrapped(user object)</h2>

```python
from letterboxdpy import user
nick = user.User("nmcassa")
print(user.user_wrapped(nick, 2023))
```

<details>
  <summary>Click to expand user_wrapped method response</summary>

```json
{
    "year": 2023,
    "logged": 120,
    "total_review": 2,
    "hours_watched": 223,
    "total_runtime": 13427,
    "first_watched": {
        "332289592": {
            "name": "The Gift",
            "slug": "the-gift-2015-1",
            "id": "255927",
            "release": 2015,
            "runtime": 108,
            "rewatched": false,
            "rating": 6,
            "liked": false,
            "reviewed": false,
            "date": {
                "year": 2023,
                "month": 1,
                "day": 1
            },
            "page": 3
        }
    },
    "last_watched": {
        "495592379": {
            ...
            ...
        }
    },
    "movies": {
        "495592379": {
            "name": "Poor Things",
            "slug": "poor-things-2023",
            "id": "710352",
            "release": 2023,
            "runtime": 141,
            "rewatched": false,
            "rating": 6,
            "liked": false,
            "reviewed": true,
            "date": {
                "year": 2023,
                "month": 12,
                "day": 26
            },
            "page": 1
        },
        ...
        ...
    },
    "months": {
        "1": 21,
        "2": 7,
        "3": 7,
        "4": 6,
        "5": 11,
        "6": 9,
        "7": 15,
        "8": 11,
        "9": 5,
        "10": 9,
        "11": 7,
        "12": 12
    },
    "days": {
        "1": 18,
        "2": 14,
        "3": 9,
        "4": 17,
        "5": 14,
        "6": 27,
        "7": 21
    },
    "milestones": {
        "50": {
            "413604382": {
                "name": "Richard Pryor: Live in Concert",
                "slug": "richard-pryor-live-in-concert",
                "id": "37594",
                "release": 1979,
                "runtime": 78,
                "rewatched": false,
                "rating": 7,
                "liked": false,
                "reviewed": false,
                "date": {
                    "year": 2023,
                    "month": 7,
                    "day": 13
                },
                "page": 2
            }
        },
        "100": {
            "347318246": {
                ...
                ...
            }
        }
    }
}
```
</details>

<h2 id="user_diary_page">user_diary_page(user object)</h2>

[To be documented.](https://github.com/search?q=repo:nmcassa/letterboxdpy+user_diary_page)

<h1 id="Members">Members Objects</h1>

[To be documented.](https://github.com/search?q=repo:nmcassa/letterboxdpy+MemberListing)

<h2 id="top_users">top_users(members object)</h2>

[To be documented.](https://github.com/search?q=repo:nmcassa/letterboxdpy+top_users)

<h1 id="Movie">Movie Objects</h1>

```python
from letterboxdpy import movie
king = movie.Movie("king kong")
print(king)
king = movie.Movie("king kong", 2005)
print(king)
house = movie.Movie("/film/the-house-2022-1/")
print(house)
```

<details>
  <summary>Click to expand Movie object response</summary>

```json
{
    "title": "king-kong",
    "url": "https://letterboxd.com/film/king-kong/",
    "directors": [
        "Merian C. Cooper",
        "Ernest B. Schoedsack"
    ],
    "rating": "3.85 out of 5",
    "year": "1933",
    "genres": [
        "horror",
        "adventure",
        "fantasy"
    ]
}
{
    "title": "king-kong-2005",
    "url": "https://letterboxd.com/film/king-kong-2005/",
    "director": "Peter Jackson",
    "rating": "3.33 out of 5",
    "year": "2005",
    "genres": [
        "action",
        "adventure",
        "drama"
    ]
}
{
    "url": "https://letterboxd.com/film/the-house-2022-1/",
    "directors": [
        "Paloma Baeza",
        "Niki Lindroth von Bahr",
        "Emma De Swaef",
        "Marc James Roels"
    ],
    "rating": "3.54 out of 5",
    "year": "2022",
    "genres": [
        "fantasy",
        "horror",
        "drama",
        "comedy",
        "animation"
    ]
}
```
</details>

<h2 id="movie_details">movie_details(movie object)</h2>

```python
from letterboxdpy import movie
king = movie.Movie("king kong", 2005)
print(movie.movie_details(king))
```

<details>
  <summary>Click to expand movie_details method response</summary>

```json
{
  "Country": [
    "New Zealand",
    "USA",
    "Germany"
  ],
  "Studio": [
    "Universal Pictures",
    "WingNut Films",
    "Big Primate Pictures",
    "MFPV Film"
  ],
  "Language": [
    "English"
  ]
}

```
</details>

<h2 id="movie_description">movie_description(movie object)</h2>

```python
from letterboxdpy import movie
king = movie.Movie("king kong", 2005)
print(movie.movie_description(king))
```

```
In 1933 New York, an overly ambitious movie producer coerces his cast and hired ship crew to travel to mysterious Skull Island, where they encounter Kong, a giant ape who is immediately smitten with...
```

<h2 id="movie_popular_reviews">movie_popular_reviews(movie object)</h2>

```python
from letterboxdpy import movie
king = movie.Movie("king kong" 2005)
print(movie.movie_popular_reviews(king))
```

<details>
  <summary>Click to expand movie_popular_reviews method response</summary>

```json
[
    {
        "reviewer":"BRAT",
        "rating":" ★★★½ ",
        "review":"naomi watts: bitch, it’s king kongking kong: yes, i’m king kongadrien brody: this is king kong?jack black: yes, miss king kong!!kyle chandler: and i’m kyle chandler :)"
    },
    {
        "reviewer":"josh lewis",
        "rating":" ★★★★ ",
        "review":"This review may contain spoilers. I can handle the truth."
    },
    {
        "reviewer":"ashley 🥀",
        "rating":" ★½ ",
        "review":"To quote one of the funniest tweets I have ever seen: did King Kong really think he was gonna date that lady?"
    },
    ...
]
```
</details>

<h2 id="movie_tmdb_link">movie_tmdb_link(movie object)</h2>

```python
from letterboxdpy import movie
rock = movie.Movie("rocky")
print(movie.movie_tmdb_link(rock))

https://www.themoviedb.org/movie/1366/
```

<h2 id="movie_watchers">movie_watchers(movie object)</h2>

[To be documented.](https://github.com/search?q=repo:nmcassa/letterboxdpy+movie_watchers)

<h2 id="movie_poster">movie_poster(movie object)</h2>

[To be documented.](https://github.com/search?q=repo:nmcassa/letterboxdpy+movie_poster)

<h1 id="List">List Objects</h1>

```python
from letterboxdpy import list
list = list.List("Horrorville", "The Official Top 25 Horror Films of 2022")
print(list)
```

<details>
  <summary>Click to expand List object response</summary>

```json
{
    "title": "the-official-top-25-horror-films-of-2022",
    "author": "horrorville",
    "url": "https://letterboxd.com/horrorville/list/the-official-top-25-horror-films-of-2022/",
    "description": "To be updated monthly. It's ranked by average Letterboxd member rating. See the official top 50 of 2021 on Horrroville here. Eligibility rules: \u2022\u00a0Feature-length narrative films included only. \u2022\u00a0Shorts, documentaries, and TV are excluded. \u2022\u00a0Films must have their festival premiere in 2022 or their first national release in any country in 2022. \u2022\u00a0Films must have the horror genre tag on TMDb and Letterboxd. \u2022\u00a0There is a 1,000 minimum view threshold. Curated by Letterboxd Head of Platform Content Jack Moulton.",
    "filmCount": 25,
    "movies": [
        [
            "Nope",
            "/film/nope/"
        ],
        [
            "Pearl",
            "/film/pearl-2022/"
        ],
        [
            "Barbarian",
           ...
```
</details>

<h2 id="list_tags">list_tags(list object)</h2>

```python
from letterboxdpy import list
a = list.List("Horrorville", "The Official Top 25 Horror Films of 2022")
print(list.list_tags(a))
```

```python
['official', 'horror', 'letterboxd official', 'letterboxd', '2022', 'topprofile', 'top 25']
```
