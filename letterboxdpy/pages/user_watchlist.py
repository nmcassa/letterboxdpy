from letterboxdpy.core.scraper import parse_url
from letterboxdpy.constants.project import DOMAIN
from letterboxdpy.pages.user_list import extract_movies
from letterboxdpy.utils.utils_parser import parse_movie_name

class UserWatchlist:
    FILMS_PER_PAGE = 7*4

    def __init__(self, username: str) -> None:
        self.username = username
        self.url = f"{DOMAIN}/{self.username}/watchlist"

    def __str__(self) -> str:
        return f"Not printable object of type: {self.__class__.__name__}"

    def get_owner(self): ...
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

    def extract_movie_info(container):
        """Extract film ID, slug, and name from watchlist container."""
        react_component = container.find("div", {"class": "react-component"}) or container.div
        if not react_component or 'data-film-id' not in react_component.attrs:
            return None
            
        movie_id = react_component['data-film-id']
        movie_slug = react_component.get('data-item-slug') or react_component.get('data-film-slug')
        movie_name = react_component.get('data-item-name') or react_component.img['alt']
        movie_year = None
        movie_name, movie_year = parse_movie_name(movie_name).values()

        return movie_id, movie_slug, movie_name, movie_year

    page = 1
    no = 1
    while True:
        dom = parse_url(f'{BASE_URL}/page/{page}')
        containers = dom.find_all("li", {"class": "griditem"}) or dom.find_all("li", {"class": ["poster-container"]})
        
        for container in containers:
            movie_info = extract_movie_info(container)
            if movie_info:
                movie_id, movie_slug, movie_name, movie_year = movie_info
                data['data'][movie_id] = {
                    'name': movie_name,
                    'slug': movie_slug,
                    'year': movie_year,
                    'page': page,
                    'url': f"{DOMAIN}/film/{movie_slug}/",
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