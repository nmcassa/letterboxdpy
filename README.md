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
    -movie's title
    -movie's year
    -user's rating on movie
    -user's review

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

## **List Object**

```python
from letterboxdpy import list
list = list.List("https://letterboxd.com/nmcassa/list/movies-for-sale-and-my-local-goodwill/")
print(list.jsonify())
```
```
{
    "title": "Movies for sale and my local goodwill",
    "author": "nmcassa",
    "description": "",
    "movies": [
        "Fiddler on the Roof",
        "Grumpier Old Men",
        "The Rainmaker",
        "Great Expectations",
        "Heat",
        "The Santa Clause",
        "The Lord of the Rings: The Fellowship of the Ring",
        "Charlie's Angels",
        "The Chamber",
        "Easy A",
        "A Christmas Carol",
        "A Christmas Story",
        "The Return of Jafar",
        "Snow Dogs",
        "101 Dalmatians",
        "Dumbo",
        "Annie",
        "Spy Kids",
        "The Lion King",
        "The Jungle Book",
        "Saving Private Ryan",
        "The Princess Diaries",
        "Aladdin and the King of Thieves",
        "Lady and the Tramp II: Scamp's Adventure",
        "Knocked Up",
        "Ocean's Eleven",
        "Evan Almighty",
        "Iron Man",
        "Crazy, Stupid, Love.",
        "Ender's Game",
        "Rambo",
        "Talladega Nights: The Ballad of Ricky Bobby",
        "National Lampoon's Christmas Vacation",
        "Mission: Impossible",
        "Mission: Impossible II",
        "Quantum of Solace",
        "The Devil Wears Prada",
        "Green Zone",
        "Inside Job",
        "Racing Stripes",
        "No Strings Attached",
        "We Bought a Zoo",
        "Madagascar",
        "Happy Feet",
        "A Cinderella Story"
    ],
    "filmCount": 45
}
```
