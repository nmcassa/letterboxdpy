# letterboxdpy

[![PyPI version](https://badge.fury.io/py/letterboxdpy.svg)](https://badge.fury.io/py/letterboxdpy)
[![Downloads](https://static.pepy.tech/personalized-badge/letterboxdpy?period=total&units=none&left_color=grey&right_color=blue&left_text=Downloads)](https://pepy.tech/project/letterboxdpy)
![format](https://img.shields.io/pypi/format/letterboxdpy)

## Installation

```
pip install letterboxdpy
```

## **User Objects**

```python
from letterboxdpy import user
nick = user.User("nmcassa")
print(nick.jsonify())
```

```
{
    "username": "nmcassa",
    "favorites": [
        "The Grand Budapest Hotel",
        "The King of Comedy",
        "The Alpinist",
        "The Graduate"
    ],
    "stats": {
        "Films": "360",
        "This year": "86",
        "List": "1",
        "Following": "7",
        "Followers": "6"
    },
    "watchlist_length": "73"
}
```

## **user_genre_info(user object)**

```python
nick = user.User("nmcassa")
print(user_genre_info(nick))
```

```
{'action': 55, 'adventure': 101, 'animation': 95, 'comedy': 188, 'crime': 22, 'documentary': 16, 'drama': 94, 'family': 109, 'fantasy': 54, 'history': 5, 'horror': 27, 'music': 9, 'mystery': 30, 'romance': 29, 'science-fiction': 48, 'thriller': 43, 'tv-movie': 13, 'war': 4, 'western': 5}
```

## **user_following(user object) / user_followers(user object)**

returns the first page of the users following / followers

## **user_films_watched(user object)**

returns all of the users watched movies

## **user_reviews(user object)**

returns a dictionary of information from reviews the user has made such as: 
- movie's title
- movie's year
- user's rating on movie
- user's review

## **Movie Object**

```python
from letterboxdpy import movie
king = movie.Movie("king kong")
print(king.jsonify())

king = movie.Movie("king kong", 2005)
print(king.jsonify())
```
```
{
    "title": "king-kong",
    "director": [
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
    "director": "Peter Jackson",
    "rating": "3.33 out of 5",
    "year": "2005",
    "genres": [
        "action",
        "adventure",
        "drama"
    ]
}

```

## **movie_details(movie object)**

```python
king = movie.Movie("king kong", 2005)
print(movie_details(king))
```
```
{'Country': ['New Zealand', 'USA', 'Germany'], 'Studio': ['Universal Pictures', 'WingNut Films', 'Big Primate Pictures', 'MFPV Film'], 'Language': ['English']}
```

## **movie_description(movie object)**

returns the description of the movie passed

## **movie_popular_reviews(movie object)**

returns information about the movie's most popular reviews, such as:
- reviewer
- rating
- review

## **List Object**

```python
from letterboxdpy import list
list = list.List("Horrorville", "The Official Top 25 Horror Films of 2022")
print(list.jsonify())
```
```
{
    "url": "https://letterboxd.com/horrorville/list/the-official-top-25-horror-films-of-2022/",
    "title": "The Official Top 25 Horror Films of 2022",
    "author": "Horrorville",
    "description": "To be updated monthly. It's ranked by average Letterboxd member rating. See the official top 50 of 2021 on Horrroville here. Eligibility rules: \u2022\u00a0Feature-length narrative films included only. \u2022\u00a0Shorts, documentaries, and TV are excluded. \u2022\u00a0Films must have their festival premiere in 2022 or their first national release in any country in 2022. \u2022\u00a0Films must have the horror genre tag on TMDb and Letterboxd. \u2022\u00a0There is a 1,000 minimum view threshold. Curated by Letterboxd Head of Platform Content Jack Moulton.",
    "movies": [
        "Nope",
        "Mad God",
        "Prey",
        "Bodies Bodies Bodies",
        "You Won't Be Alone",
        "X",
        "The House",
        "Fresh",
        "Final Cut",
        "Saloum",
        "The Black Phone",
        "Bhoothakaalam",
        "Nanny",
        "Resurrection",
        "15 Ways to Kill Your Neighbour",
        "Speak No Evil",
        "Watcher",
        "Scream",
        "Crimes of the Future",
        "Flux Gourmet",
        "Medusa",
        "What Josiah Saw",
        "Satan's Slaves 2: Communion",
        "Piggy",
        "Dawn Breaks Behind the Eyes"
    ],
    "filmCount": 25
}
```

## **list_tags(list object)**

returns the tags under the list
