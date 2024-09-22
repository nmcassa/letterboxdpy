from datetime import datetime

# Date/Time Constants
CURRENT_YEAR = datetime.now().year
MONTH_ABBREVIATIONS = [
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
]

# Domain/URL Constants
DOMAIN = "https://letterboxd.com"

# Movie-Related Constants
VALID_RATINGS = {0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5}
GENRES = [
    "action", "adventure", "animation", "comedy", "crime",
    "documentary", "drama", "family", "fantasy", "history",
    "horror", "music", "mystery", "romance", "science-fiction",
    "thriller", "tv-movie", "war", "western"
]
