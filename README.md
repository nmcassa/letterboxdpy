# letterboxdpy

[![PyPI version](https://badge.fury.io/py/letterboxdpy.svg)](https://badge.fury.io/py/letterboxdpy)
[![Downloads](https://static.pepy.tech/personalized-badge/letterboxdpy?period=total&units=none&left_color=grey&right_color=blue&left_text=Downloads)](https://pepy.tech/project/letterboxdpy)
![format](https://img.shields.io/pypi/format/letterboxdpy)

## Installation

```
pip install letterboxdpy
```

## **Code Example**

```python
from letterboxdpy import user
nick = user.User("nmcassa")
print(nick.jsonify())
```

### **User Object JSON**

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
        "Films": "342",
        "This year": "69",
        "List": "1",
        "Following": "6",
        "Followers": "5"
    }
}
```

## ** Code Example**

```python
nick = user.User("nmcassa")
print(nick.user_genre_info())
```

### Output

```
{'action': 55, 'adventure': 101, 'animation': 95, 'comedy': 188, 'crime': 22, 'documentary': 16, 'drama': 94, 'family': 109, 'fantasy': 54, 'history': 5, 'horror': 27, 'music': 9, 'mystery': 30, 'romance': 29, 'science-fiction': 48, 'thriller': 43, 'tv-movie': 13, 'war': 4, 'western': 5}
```

## **Code Example**

```python
from letterboxdpy import movie
king = movie.Movie("king kong")
print(king.jsonify())

king = movie.Movie("king kong", 2005)
print(king.jsonify())
```

### **Movie Object JSON**

```
{
    "title": "king-kong",
    "director": [
        "Merian C. Cooper",
        "Ernest B. Schoedsack"
    ],
    "rating": "3.85 out of 5",
    "description": "A film crew discovers the \"eighth wonder of the world,\" a giant prehistoric ape, and brings him back to New York, where he wreaks havoc.",
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
    "rating": "3.32 out of 5",
    "description": "In 1933 New York, an overly ambitious movie producer coerces his cast and hired ship crew to travel to mysterious Skull Island, where they encounter Kong, a giant ape who is immediately smitten with...",
    "year": "2005",
    "genres": [
        "action",
        "adventure",
        "drama"
    ]
}
```

## **Code Example**

```python
king = movie.Movie("king kong", 2005)
print(king.movie_details())
```

### **Output**

```
{'Country': ['New Zealand', 'USA', 'Germany'], 'Studio': ['Universal Pictures', 'WingNut Films', 'Big Primate Pictures', 'MFPV Film'], 'Language': ['English']}
```

## **Code Example**

```python
from letterboxdpy import list
list = list.List("https://letterboxd.com/nmcassa/list/movies-for-sale-and-my-local-goodwill/")
print(list.jsonify())
```

### **List Object JSON**

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
