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
 - [Movie Objects](#Movie)
 - [List Objects](#List)

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

## **user_genre_info(user object)**

```python
from letterboxdpy import user
nick = user.User("nmcassa")
print(user.user_genre_info(nick))
```

<details>
  <summary>Click to expand user_genre_info method response</summary>

```python
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

## **user_following(user object) / user_followers(user object)**

```python
from letterboxdpy import user
nick = user.User("nmcassa")
print(user.user_following(nick))
print(user.user_followers(nick))
```

<details>
  <summary>Click to expand user_following & user_followers methods response</summary>

```python
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

## **user_films_watched(user object)**

```python
from letterboxdpy import user
nick = user.User("nmcassa")
print(user.user_films_watched(nick))
```

<details>
  <summary>Click to expand user_films_watched method response</summary>

```python
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

## **user_reviews(user object)**

```python
from letterboxdpy import user
nick = user.User("nmcassa")
print(user.user_reviews(nick))
```

<details>
  <summary>Click to expand user_reviews method response</summary>

```python
{
    "reviews": {
        "poor-things-2023": {
            "movie": "Poor Things",
            "movie_id": "710352",
            "movie_year": 2023,
            "rating": 6,
            "review": "It looks like AI art and weird movie",
            "date": "26 Dec 2023"
        },
        "sisu-2022": {
            "movie": "Sisu",
            "movie_id": "755504",
            "movie_year": 2022,
            "rating": 5,
            "review": "gross",
            "date": "03 May 2023"
        },...
    },
    "count": 7,
    "last_page": 1
}
```
</details>

## **user_diary and user_diary_page and user_films_rated**

 To be documented.

## **Member Listing and top_users **

 To be documented.

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

## **movie_details(movie object)**

```python
from letterboxdpy import movie
king = movie.Movie("king kong", 2005)
print(movie.movie_details(king))
```

```python
{'Country': ['New Zealand', 'USA', 'Germany'], 'Studio': ['Universal Pictures', 'WingNut Films', 'Big Primate Pictures', 'MFPV Film'], 'Language': ['English']}
```

## **movie_description(movie object)**

```python
from letterboxdpy import movie
king = movie.Movie("king kong", 2005)
print(movie.movie_description(king))
```

```
In 1933 New York, an overly ambitious movie producer coerces his cast and hired ship crew to travel to mysterious Skull Island, where they encounter Kong, a giant ape who is immediately smitten with...
```

## **movie_popular_reviews(movie object)**

```python
from letterboxdpy import movie
king = movie.Movie("king kong" 2005)
print(movie.movie_popular_reviews(king))
```

<details>
  <summary>Click to expand movie_popular_reviews method response</summary>

```
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

## **movie_tmdb_link**

```python
from letterboxdpy import movie
rock = movie.Movie("rocky")
print(movie.movie_tmdb_link(rock))

https://www.themoviedb.org/movie/1366/
```

## **movie_watchers**

 To be documented 

## **movie_poster**

 To be documented.

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

## **list_tags(list object)**

```python
from letterboxdpy import list
a = list.List("Horrorville", "The Official Top 25 Horror Films of 2022")
print(list.list_tags(a))
```

```python
['official', 'horror', 'letterboxd official', 'letterboxd', '2022', 'topprofile', 'top 25']
```
