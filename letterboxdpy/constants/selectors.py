"""
CSS and HTML selectors for web scraping.

Defines BeautifulSoup selectors used to extract data from
Letterboxd pages including films, metadata, and error messages.
"""

from dataclasses import dataclass


Selector = tuple[str, dict[str, str]]

@dataclass
class FilmSelectors:
    """Selectors for film list elements"""
    # <div class="list-detailed-entries-list js-list-entries">
    LIST: Selector = ('div', {'class': 'js-list-entries'})
    # <h2 class="name -primary prettify"><a href="/film/aliens-vs-predator-requiem/">Aliens vs Predator: Requiem</a></h2>
    HEADLINE: Selector = ('h2', {'class': 'name'})
    # <span class="releasedate"><a href="/films/year/2007/">2007</a></span>
    YEAR: Selector = ('span', {'class': 'releasedate'})

@dataclass
class MetaSelectors:
    """Selectors for meta elements"""
    DESCRIPTION: Selector = ('meta', {'name': 'description'})

@dataclass
class PageSelectors:
    """Selectors for page elements"""
    ERROR_BODY: Selector = ('body', {'class': 'error'})
    ERROR_MESSAGE: Selector = ('section', {'class': 'message'})
    LAST_PAGE: Selector = ('div', {'class': 'paginate-pages'})
    ARTICLES: Selector = ('ul', {'class': 'poster-list -p70 film-list clear film-details-list'}) 
