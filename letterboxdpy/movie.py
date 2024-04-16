from letterboxdpy.scraper import Scraper
from functools import wraps

from json import (
  JSONEncoder,
  dumps as json_dumps,
  loads as json_loads,
)
from url import fetch_stats_url
from utils import extract_numeric_text

class Movie:
    DOMAIN = 'https://letterboxd.com'

    def __init__(self, slug: str) -> None:
        assert isinstance(slug, str), f"Movie slug must be a string, not {type(slug)}"

        self.scraper = Scraper(self.DOMAIN)
        self.url = f'{self.DOMAIN}/film/{slug}'
        self.slug = slug

        dom = self.scraper.get_parsed_page(self.url)

        script = dom.find("script", type="application/ld+json")
        script = json_loads(script.text.split('*/')[1].split('/*')[0]) if script else None

        # one line contents
        self.movie_title_id(script)
        self.movie_title(dom)
        self.movie_original_title(dom)
        self.movie_runtime(dom)
        self.movie_rating(dom, script)
        self.movie_year(dom, script)
        self.movie_tmdb_link(dom)
        self.movie_imdb_link(dom)
        self.movie_poster(script)
        # long contents
        self.movie_tagline(dom)
        self.movie_description(dom)
        self.movie_alternative_titles(dom)
        self.movie_stats()
        self.movie_details(dom)
        self.movie_genres(dom)
        self.movie_cast(dom)
        self.movie_crew(dom)
        self.movie_popular_reviews(dom)

    def __str__(self):
        return self.jsonify()

    def jsonify(self) -> str:
        return json_dumps(self, indent=2, cls=Encoder)

    # letterboxd.com/film/?
    def movie_cast(self, dom) -> list:
        data = dom.find("div", {"id": ["tab-cast"]})
        data = data.find_all("a", {"class": {"tooltip"}}) if data else []

        cast = []
        for person in data:

            name = person.text
            role_name = person['title'] if 'title' in person.attrs else None
            url = person['href']
            slug = url.split('/')[-2]
            
            cast.append({
                'name': name,
                'role_name': role_name,
                'slug': slug,
                'url': self.DOMAIN + url}
                )

        self.cast = cast

    # letterboxd.com/film/?
    def movie_crew(self, dom) -> list:
        data = dom.find("div", {"id": ["tab-crew"]})
        data = data.find_all("a") if data else []

        crew = {}
        for person in data:
            name = person.text
            url = person['href']
  
            job, slug = filter(None, url.split('/'))
            job = job.replace('-', '_')

            if job not in crew:
                crew[job] = []

            crew[job].append({
                'name': name,
                'slug': slug,
                'url': self.DOMAIN + url}
                )

        self.crew = crew

    # letterboxd.com/film/?
    def movie_details(self, dom) -> dict:
        data = dom.find("div", {"id": ["tab-details"]})
        data = data.find_all("a") if data else []

        details = []
        for item in data:
            url_parts = item['href'].split('/')

            _ =  url_parts[1] == 'films'
            item_type, slug = url_parts[1+_:3+_] 

            details.append({
                'type': item_type,
                'name': item.text,
                'slug': slug,
                'url': self.DOMAIN + "/".join(url_parts)
            })

        self.details = details

    # letterboxd.com/film/?
    def movie_alternative_titles(self, dom):
        data = dom.find(attrs={'class': 'text-indentedlist'})
        text = data.text if data else None
        titles = [i.strip() for i in text.split(', ')] if text else None
        self.alternative_titles = titles

    # letterboxd.com/film/?
    def movie_genres(self, dom) -> list:
        data = dom.find(attrs={"id": ["tab-genres"]})
        data = data.find_all("a") if data else None

        genres = []
        if data is not None:
            for item in data:
                url_parts = item['href'].split('/')
                
                genres.append({
                    'type': url_parts[2],
                    'name': item.text,
                    'slug': url_parts[3],
                    'url': self.DOMAIN + "/".join(url_parts)
                })

        if genres and self.slug == genres[-1]['type']:
            genres.pop() # for show all button

        self.genres = genres

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
        try:
            year = year if year else (
                script['releasedEvent']['startDate'] if script else None
                )
            self.year = int(year)
        except KeyError:
            self.year = None

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
    def movie_tagline(self, dom) -> str:
        elem = dom.find(attrs={'class':'tagline'})
        self.tagline = elem.text if elem else None

    # letterboxd.com/film/?
    def movie_description(self, dom) -> str:
        elem = dom.find("meta", attrs={'name':'description'})
        # elem_section = page.find("div", attrs={'class': 'truncate'}).text
        self.description = elem['content'] if elem else None

    # letterboxd.com/csi/film/?/stats
    def movie_stats(self) -> int:
        stats_url = fetch_stats_url(self.movie_title_id)
        stats_dom = self.scraper.get_parsed_page(url=stats_url)
        self.watch_count = extract_numeric_text(stats_dom.find('li', 'filmstat-watches').a.get('title'))
        self.list_count = extract_numeric_text(stats_dom.find('li', 'filmstat-lists').a.get('title'))
        self.like_count = extract_numeric_text(stats_dom.find('li', 'filmstat-likes').a.get('title'))

    # letterboxd.com/film/?
    def movie_popular_reviews(self, dom) -> dict:
        data = dom.find("ul", {"class": ["film-popular-review"]})
        items = data.find_all("div", {"class": ["film-detail-content"]}) if data else []

        self.popular_reviews = []
        for item in items:
            curr = {}

            owner = item.find("strong", {"class": ["name"], })
            rating = item.find("span", {"class": ['rating'], })
            review = item.find("div", {"class": ['body-text'], })
            review = review.p if review is not None else None

            curr['reviewer'] = owner.text if owner else None
            curr['rating'] = rating.text if rating else None
            curr['review'] = review.text if review else None

            self.popular_reviews.append(curr)

    def movie_title_id(self, script) -> str:
        try:
            self.movie_title_id = script['url'].split('/')[4]
        except Exception as e:
            print(f"Error occurred while parsing movie title id: {e}")
            self.movie_title_id = ''

    # letterboxd.com/film/?
    def movie_title(self, dom) -> int:
        elem = dom.find("section", {"id": ["featured-film-header"]})
        elem = elem.find("h1")
        elem = elem.text if elem else None
        self.title = elem.strip()

    # letterboxd.com/film/?
    def movie_original_title(self, dom) -> int:
        elem = dom.find("section", {"id": ["featured-film-header"]})
        elem = elem.find("em")
        elem = elem.text.strip("'’‘ ") if elem else None
        self.original_title = elem
      
    # letterboxd.com/film/?
    def movie_runtime(self, dom) -> int:
        elem = dom.find("p", {"class": ["text-footer"]})
        elem = elem.find_all(string=True, recursive=False)
        for i in elem:
            if 'min' in i.text:
                self.runtime = int(i.split('min')[0].replace(',','').strip())
                return
        self.runtime = None

    # letterboxd.com/film/?
    def movie_tmdb_link(self, dom) -> str:
        a = dom.find("a", {"data-track-action": ["TMDb"]})
        self.tmdb_link = a['href'] if a else None

    # letterboxd.com/film/?
    def movie_imdb_link(self, dom) -> str:
        a = dom.find("a", {"data-track-action": ["IMDb"]})
        self.imdb_link = a['href'] if a else None

class Encoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

# -- DECORATORS --

def assert_movie_instance(func):
    @wraps(func)
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
        'watch_count': movie.watch_count if movie.watch_count else 0,
        'fan_count': 0,
        'like_count': movie.like_count if movie.like_count else 0,
        'review_count': 0,
        'list_count': movie.list_count if movie.list_count else 0
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
