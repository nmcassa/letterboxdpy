# letterboxdpy

[![PyPI version](https://badge.fury.io/py/letterboxdpy.svg)](https://badge.fury.io/py/letterboxdpy)
[![Downloads](https://static.pepy.tech/personalized-badge/letterboxdpy?period=month&units=none&left_color=grey&right_color=blue&left_text=Downloads)](https://pepy.tech/project/letterboxdpy)
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
