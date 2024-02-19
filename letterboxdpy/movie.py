from letterboxdpy.scraper import Scraper

from json import (
  JSONEncoder,
  dumps as json_dumps,
  loads as json_loads,
)


class Movie:
    DOMAIN = 'https://letterboxd.com'

    def __init__(self, slug: str) -> None:
        assert isinstance(slug, str), f"Movie slug must be a string, not {type(slug)}"

        self.url = f'{self.DOMAIN}/film/{slug}'
        self.scraper = Scraper(self.DOMAIN)

        dom = self.scraper.get_parsed_page(self.url)

        script = dom.find("script", type="application/ld+json")
        script = json_loads(script.text.split('*/')[1].split('/*')[0]) if script else None

        # one line contents
        self.movie_tmdb_link(dom)
        self.movie_poster(script)
        self.movie_rating(dom, script)
        self.movie_year(dom, script)
        # long contents
        self.movie_description(dom)
        self.movie_director(dom)
        self.movie_genre(dom)
        self.movie_popular_reviews(dom)

    def __str__(self):
        return self.jsonify()

    def jsonify(self) -> str:
        return json_dumps(self, indent=2, cls=Encoder)

    # letterboxd.com/film/?
    def movie_director(self, dom) -> list:
        self.directors = []
        data = dom.find("div",{"id": ["tab-crew"], })
        if type(data) != type(None):
            data = data.find_all("a")
            for item in data:
                if item['href'][:10] == '/director/':
                    self.directors.append(item.text)

    # letterboxd.com/film/?
    def movie_rating(self, dom, script: dict=None) -> float:
        elem = dom.find('span', attrs={'class': 'average-rating'})
        rating = elem.text if elem else None
        try:
            rating = rating if rating else (
                script['aggregateRating']['ratingValue'] if script else None
                )
            self.rating = float(rating)
        except KeyError:
            self.rating = None

    # letterboxd.com/film/?
    def movie_year(self, dom, script: dict=None) -> int:
        elem = dom.find('small', attrs={'class': 'number'})
        year = int(elem.text) if elem else None
        year = year if year else (
             script['releasedEvent']['startDate'] if script else None
             )
        self.year = int(year)

    # letterboxd.com/film/?
    def movie_genre(self, dom) -> list:
        genres = []

        data = dom.find("div",{"id": ["tab-genres"], })
        if data is not None:
            data = data.find_all("a")
            for item in data:
                if item['href'][7:12] == 'genre':
                    genres.append(item.text)
        self.genres = genres

    # letterboxd.com/film/?
    def movie_poster(self, script) -> str:
        # crop: list=(1500, 1000)
        # .replace('230-0-345', f'{crop[0]}-0-{crop[1]}')
        if script:
            poster = script['image'] if 'image' in script else None
            self.poster = poster.split('?')[0] if poster else None
        else:
            self.poster = None

    # letterboxd.com/film/?
    def movie_description(self, dom) -> str:
        elem = dom.find("meta", attrs={'name':'description'})
        # elem_section = page.find("div", attrs={'class': 'truncate'}).text
        self.description = elem['content'] if elem else None

    # letterboxd.com/film/?
    def movie_popular_reviews(self, dom) -> dict:
        data = dom.find("ul", {"class": ["film-popular-review"]})
        items = data.find_all("div", {"class": ["film-detail-content"]}) if data else []

        self.popular_reviews = []
        for item in items:
            curr = {}

            owner = item.find("strong", {"class": ["name"], })
            rating = item.find("span", {"class": ['rating'], })
            review = item.find("div", {"class": ['body-text'], }).p

            curr['reviewer'] = owner.text if owner else None
            curr['rating'] = rating.text if rating else None
            curr['review'] = review.text if review else None

            self.popular_reviews.append(curr)

    # letterboxd.com/film/?
    def movie_tmdb_link(self, dom) -> str:
        try:
            div = dom.find("p", {"class": ["text-link text-footer"]})
            for a in div.find_all("a"):
                if a['href'].find('themoviedb.org/') != -1:
                    self.tmdb_link = (a['href']) 
        except: 
            self.tmdb_link = None

class Encoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

# -- DECORATORS --

def assert_movie_instance(func):
    def wrapper(movie):
        assert isinstance(movie, Movie), f"movie parameter must be a {Movie.__name__} instance"
        return func(movie)
    return wrapper

# -- FUNCTIONS --

# letterboxd.com/film/?/details
@assert_movie_instance
def movie_details(movie: Movie) -> dict:
    dom = movie.scraper.get_parsed_page("/".join([movie.url, "details"]))
    dom = dom.find("div", {"id": ["tab-details"]})

    data = {
        'country': [],
        'studio': [],
        'language': []
    }

    for a in dom.find_all("a"):
        if a['href'][1:7] == 'studio':
            data['studio'].append(a.text)
        elif a['href'][7:14] == 'country':
            data['country'].append(a.text)
        elif a['href'][7:15] == 'language':
            data['language'].append(a.text)

    return data

# letterboxd.com/film/?/members
@assert_movie_instance
def movie_watchers(movie: Movie) -> dict:
    dom = movie.scraper.get_parsed_page("/".join([movie.url, "members"]))
    dom = dom.find("div", {"id": ["content-nav"]})

    data = {
        'watch_count': 0,
        'fan_count': 0,
        'like_count': 0,
        'review_count': 0,
        'list_count': 0
    }

    if dom:
        for a in dom.find_all("a"):
            if a.get('title'):
                if a['title'].find('people',-6) != -1:
                    data['watch_count'] = a['title'][:-7].replace(',','')
                elif a['title'].find('fans',-4) != -1:
                    data['fan_count'] = a['title'][:-5].replace(',','')
                elif a['title'].find('likes',-5) != -1:
                    data['like_count'] = a['title'][:-6].replace(',','')
                elif a['title'].find('reviews',-7) != -1:
                    data['review_count'] = a['title'][:-8].replace(',','')
                elif a['title'].find('lists',-5) != -1:
                    data['list_count'] = a['title'][:-6].replace(',','')
    return data

if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding='utf-8')

    movie_instance = Movie("v-for-vendetta")
    print(movie_instance)
    print(movie_details(movie_instance))
    print(movie_watchers(movie_instance))