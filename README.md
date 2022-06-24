# letterboxdpy

[![PyPI version](https://badge.fury.io/py/letterboxdpy.svg)](https://badge.fury.io/py/letterboxdpy)

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

### Output

![Example of the user object](ss/user_example.PNG)

## **Code Example**

```python
from letterboxdpy import movie
king = movie.Movie("king kong")
print(king.jsonify())

king = movie.Movie("king kong", 2005)
print(king.jsonify())
```

## **Example of Movie Object**

![Example of the movie object](ss/movie_example.PNG)
