import json
import requests
from bs4 import BeautifulSoup
from json import JSONEncoder


class Movie:
    DOMAIN = 'https://letterboxd.com'
    FILM_URL = DOMAIN + '/film/'

    def __init__(self, slug: str) -> None:
        self.url = self.FILM_URL + slug
        page = self.get_parsed_page(self.url)

        script = page.find("script", type="application/ld+json")
        script = json.loads(script.text.split('*/')[1].split('/*')[0]) if script else None

        # one line contents
        self.movie_tmdb_link(page)
        self.movie_poster(script)
        self.movie_rating(page, script)
        self.movie_year(page, script)
        # long contents
        self.movie_description(page)
        self.movie_director(page)
        self.movie_genre(page)
        self.movie_popular_reviews(page)

    def __str__(self):
        return self.jsonify()

    def jsonify(self) -> str:
        return json.dumps(self, indent=4,cls=Encoder)

    def get_parsed_page(self, url: str) -> None:
        # This fixes a blocked by cloudflare error i've encountered
        headers = {
            "referer": self.DOMAIN,
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        response = requests.get(url, headers=headers)
        return BeautifulSoup(response.text, "lxml")

    # letterboxd.com/film/?
    def movie_director(self, page: BeautifulSoup) -> list:
        self.directors = []
        data = page.find("div",{"id": ["tab-crew"], })
        if type(data) != type(None):
            data = data.find_all("a")
            for item in data:
                if item['href'][:10] == '/director/':
                    self.directors.append(item.text)

    # letterboxd.com/film/?
    def movie_rating(self, page: BeautifulSoup, script: dict=None) -> float:
        elem = page.find('span', attrs={'class': 'average-rating'})
        rating = float(elem.text) if elem else None
        rating = rating if rating else (
             script['aggregateRating']['ratingValue'] if script else None
             )
        self.rating = float(rating)

    # letterboxd.com/film/?
    def movie_year(self, page: BeautifulSoup, script: dict=None) -> int:
        elem = page.find('small', attrs={'class': 'number'})
        year = int(elem.text) if elem else None
        year = year if year else (
             script['releasedEvent']['startDate'] if script else None
             )
        self.year = int(year)

    # letterboxd.com/film/?
    def movie_genre(self, page: BeautifulSoup) -> list:
        genres = []

        data = page.find("div",{"id": ["tab-genres"], })
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
            poster = script['image']
            self.poster = poster.split('?')[0] if poster else None
        else:
            self.poster = None

    # letterboxd.com/film/?
    def movie_description(self, page: BeautifulSoup) -> str:
        elem = page.find("meta", attrs={'name':'description'})
        # elem_section = page.find("div", attrs={'class': 'truncate'}).text
        self.description = elem['content'] if elem else None

    # letterboxd.com/film/?
    def movie_popular_reviews(self, page: BeautifulSoup) -> dict:
        data = page.find("ul", {"class": ["film-popular-review"], })
        data = data.find_all("div", {"class": ["film-detail-content"], })

        self.popular_reviews = []
        for item in data:
            curr = {}

            try:
                curr['reviewer'] = item.find("strong", {"class": ["name"], }).text
            except:
                curr['reviewer'] = None

            try:
                curr['rating'] = item.find("span", {"class": ['rating'], }).text
            except:
                curr['rating'] = None

            try:
                curr['review'] = item.find("div", {"class": ['body-text'], }).findChild("p").text
            except:
                curr['review'] = None

            self.popular_reviews.append(curr)

    # letterboxd.com/film/?
    def movie_tmdb_link(self, page: BeautifulSoup) -> str:
        try:
            div = page.find("p", {"class": ["text-link text-footer"], })
            a = div.find_all("a")
            for item in a:
                if item['href'].find('themoviedb.org/') != -1:
                    self.tmdb_link = (item['href']) 
        except: 
            self.tmdb_link = None

# letterboxd.com/film/?/details
def movie_details(movie: Movie) -> dict:
    if type(movie) != Movie:
        raise Exception("Improper parameter")

    page = movie.get_parsed_page("/".join([movie.url, "details"]))

    res = {}
    studio = []
    country = []
    language = []

    div = page.find("div", {"id": ["tab-details"], })
    a = div.find_all("a")

    for item in a:
        if item['href'][1:7] == 'studio':
            studio.append(item.text)
        elif item['href'][7:14] == 'country':
            country.append(item.text)
        elif item['href'][7:15] == 'language':
            language.append(item.text)

    res['Country'] = country
    res['Studio'] = studio
    res['Language'] = language

    return res

# letterboxd.com/film/?/members
def movie_watchers(movie: Movie) -> dict:
    if type(movie) != Movie:
        raise Exception("Improper parameter")

    page = movie.get_parsed_page("/".join([movie.url, "members"]))

    res = {}
    res['watch_count'] = 0
    res['fan_count'] = 0
    res['like_count'] = 0
    res['review_count'] = 0
    res['list_count'] = 0

    div = page.find("div", {"id": ["content-nav"], })
    if type(div) != type(None):
        a = div.find_all("a")

        for item in a:
            if item.get('title'):
                if item['title'].find('people',-6) != -1:
                    res['watch_count'] = item['title'][:-7].replace(',','')
                elif item['title'].find('fans',-4) != -1:
                    res['fan_count'] = item['title'][:-5].replace(',','')
                elif item['title'].find('likes',-5) != -1:
                    res['like_count'] = item['title'][:-6].replace(',','')
                elif item['title'].find('reviews',-7) != -1:
                    res['review_count'] = item['title'][:-8].replace(',','')
                elif item['title'].find('lists',-5) != -1:
                    res['list_count'] = item['title'][:-6].replace(',','')
    return res

class Encoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding='utf-8')

    movie_instance = Movie("v-for-vendetta")
    print(movie_instance)
    print(movie_details(movie_instance))
    print(movie_watchers(movie_instance))