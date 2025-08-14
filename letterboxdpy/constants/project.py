from datetime import datetime

# Date/Time Constants
now = datetime.now()
CURRENT_YEAR = now.year
CURRENT_MONTH = now.month
CURRENT_DAY = now.day
MONTH_ABBREVIATIONS = [
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
]

# Domain/URL Constants
URL_PROTOCOLS = ['http://', 'https://']

DOMAIN_FULL = 'letterboxd.com'
DOMAIN_SHORT = 'boxd.it'

# Base URLs
DOMAIN = f'https://{DOMAIN_FULL}'
SITE = f'{DOMAIN}/'
SITE_SHORT = f'https://{DOMAIN_SHORT}/'

DOMAIN_MATCHES = [f'{DOMAIN_FULL}/', f'{DOMAIN_SHORT}/']

# Movie-Related Constants
VALID_RATINGS = {0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5}
GENRES = [
    "action", "adventure", "animation", "comedy", "crime",
    "documentary", "drama", "family", "fantasy", "history",
    "horror", "music", "mystery", "romance", "science-fiction",
    "thriller", "tv-movie", "war", "western"
]

# Letterboxd Theme Colors
class Colors:
    BG = '#14181C'        # Letterboxd dark background
    BLUE = '#456'         # Letterboxd blue
    GREEN = '#00C030'     # Letterboxd green
    TEXT = '#9AB'         # Letterboxd text gray