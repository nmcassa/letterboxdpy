"""
Page parser for user watchlist.
Extracts watchlist data by scraping Letterboxd HTML pages.
"""
from letterboxdpy.core.scraper import parse_url
from letterboxdpy.constants.project import DOMAIN
from letterboxdpy.pages.user_list import extract_movies
from letterboxdpy.utils.utils_url import get_page_url

class UserWatchlist:
    FILMS_PER_PAGE = 7*4

    def __init__(self, username: str) -> None:
        self.username = username
        self.url = f"{DOMAIN}/{self.username}/watchlist"

    def __str__(self) -> str:
        return f"Not printable object of type: {self.__class__.__name__}"

    def get_owner(self) -> str: return self.username
    def get_count(self) -> int: return extract_count(self.url)
    def get_movies(self) -> dict: return extract_movies(self.url, self.FILMS_PER_PAGE)
    def get_watchlist(self, filters: dict=None) -> dict: return extract_watchlist(self.username, filters)

def extract_count(url: str) -> int:
    """Extracts the number of films from the watchlist page's DOM."""
    dom = parse_url(url)

    watchlist_div = dom.find("div", class_="s-watchlist-content")
    if watchlist_div and "data-num-entries" in watchlist_div.attrs:
        return int(watchlist_div["data-num-entries"])

    count_span = dom.find("span", class_="js-watchlist-count")

    if count_span:
        count = count_span.text.split()[0]
        return int(count.replace(",", ""))

    raise ValueError("Watchlist count could not be extracted from DOM")

def extract_watchlist(username: str, filters: dict = None) -> dict:
    """
    Extracts a user's watchlist from the platform.

    filter examples:
        - keys: decade, year, genre

        # positive genre & negative genre (start with '-')
        - {genre: ['mystery']}  <- same -> {genre: 'mystery'}
        - {genre: ['-mystery']} <- same -> {genre: '-mystery'}

        # multiple genres
        - {genre: ['mystery', 'comedy'], decade: '1990s'}
        - {genre: ['mystery', '-comedy'], year: '2019'}
        - /decade/1990s/genre/action+-drama/
          ^^---> {'decade':'1990s','genre':['action','-drama']}
    """
    data = {
        'available': False,
        'count': 0,
        'last_page': None,
        'filters': filters,
        'data': {}
    }

    FILMS_PER_PAGE = 28  # Total films per page (7 rows * 4 columns)
    BASE_URL = f"{DOMAIN}/{username}/watchlist/"

    # Construct the URL with filters if provided
    if filters and isinstance(filters, dict):
        f = ""
        for key, values in filters.items():
            if not isinstance(values, list):
                values = [values]
            f += f"{key}/"
            f += "+".join([str(v) for v in values]) + "/"
        BASE_URL += f

    def extract_movie_info(container) -> dict[str, str | int | None] | None:
        """Extract film ID, slug, name, and year from watchlist container.
        
        Returns:
            dict: {"id": str, "slug": str, "name": str, "year": int|None} or None if extraction fails
                
        Example:
            Input: container with "The Matrix (1999)"
            Output: {"id": "12345", "slug": "the-matrix", "name": "The Matrix", "year": 1999}
        """
        from letterboxdpy.utils.utils_string import extract_year_from_movie_name, clean_movie_name
        
        data = container.find("div", {"class": "react-component"}) or container.div
        if not data or 'data-film-id' not in data.attrs:
            return None
            
        raw_name = data.get('data-item-name') or data.img['alt']
        name = clean_movie_name(raw_name)
        year = extract_year_from_movie_name(raw_name)
        
        context = {
            "id": data['data-film-id'],
            "slug": data.get('data-item-slug') or data.get('data-film-slug'),
            "name": name,
            "year": year
        }
        
        return context

    page = 1
    no = 1
    while True:
        dom = parse_url(get_page_url(BASE_URL, page))
        containers = dom.find_all("li", {"class": "griditem"}) or dom.find_all("li", {"class": ["poster-container"]})
        
        for container in containers:
            movie_info = extract_movie_info(container)
            if movie_info:
                data['data'][movie_info["id"]] = {
                    'name': movie_info["name"],
                    'slug': movie_info["slug"],
                    'year': movie_info["year"],
                    'page': page,
                    'url': f"{DOMAIN}/film/{movie_info['slug']}/",
                    'no': no
                }
                no += 1

        if len(containers) < FILMS_PER_PAGE:
            break
        page += 1

    # Set the count of films and availability
    data['count'] = len(data['data'])
    data['available'] = data['count'] > 0
    data['last_page'] = page

    # Reverse numbering for films
    for fv in data['data'].values():
        fv.update({'no': data['count'] - fv['no'] + 1})

    return data
