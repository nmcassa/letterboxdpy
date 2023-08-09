import json
import re
import requests
from bs4 import BeautifulSoup
from json import JSONEncoder

class Movie:
    def __init__(self, title: str, year: str = '') -> None:
        if title[0] == "/":
            self.url = "https://letterboxd.com" + title
        else:
            if year != '':
                title = title + ' ' + str(year)
            self.title = title.replace(' ', '-').lower()
            self.url = "https://letterboxd.com/film/" + self.title + "/"

        page = self.get_parsed_page(self.url)

        if not self.check_year(year, page):
            year = ''
        
        self.movie_director(page)
        self.movie_rating(page)
        self.movie_year(page)
        self.movie_genre(page)

    def __str__(self):
        return self.jsonify()

    def jsonify(self) -> str:
        return json.dumps(self, indent=4,cls=Encoder)

    def get_parsed_page(self, url: str) -> None:
        # This fixes a blocked by cloudflare error i've encountered
        headers = {
            "referer": "https://letterboxd.com",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }

        return BeautifulSoup(requests.get(url, headers=headers).text, "lxml")

    def movie_director(self, page: None) -> str or list:
        try:
            data = page.find_all("span", text = 'Director')
            director = data[0].parent.parent.findChildren("a")
            self.director = director[0].text
        except:
            data = page.find_all("span", text = 'Directors')
            if len(data) == 0: #check for no directors
                return []
            directors = data[0].parent.parent.findChildren("p")[0]
            directors = directors.findChildren("a")
            self.directors = []
            for item in directors:
                self.directors.append(item.text)

    def movie_rating(self, page: None) -> str:
        try:
            data = page.find_all("meta", attrs={'name':'twitter:data2'})
            self.rating = data[0]['content']
        except:
            self.rating = "None found"

    def movie_year(self, page: None) -> str:
        try:
            data = page.find_all("meta", attrs={'name': 'twitter:title'})
            data = data[0]['content']
            self.year = data[data.find('(')+1:data.find(')')]
        except:
            self.year = "None found"

    def check_year(self, year: str, page: None) -> bool:
        try:
            data = page.find_all("meta", attrs={'name': 'twitter:title'})
            data = data[0]['content']
            true_year = data[data.find('(')+1:data.find(')')]
        except:
            return True

        if str(true_year) != str(year) and year != '':
            return False
        return True

    def movie_genre(self, page: None) -> list:
        res = []

        data = page.find("div",{"id": ["tab-genres"], })
        try:
            data = data.find_all("a")
        except:
            raise Exception("No movie found")

        for item in data:
            if item['href'][7:12] == 'genre':
                res.append(item.text)

        self.genres = res

def movie_popular_reviews(movie: Movie) -> dict:
    if type(movie) != Movie:
        raise Exception("Improper parameter")

    ret = []

    page = movie.get_parsed_page(movie.url)

    data = page.find("ul", {"class": ["film-popular-review"], })
    data = data.find_all("div", {"class": ["film-detail-content"], })

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

        ret.append(curr)

    return ret

def movie_details(movie: Movie) -> dict:
    if type(movie) != Movie:
        raise Exception("Improper parameter")

    page = movie.get_parsed_page(movie.url + "details/")

    res = {}
    studio = []
    country = []
    language = []

    div = page.find("div", {"id": ["tab-details"], })
    a = div.find_all("a")

    for item in a:
        if item['href'][1:7] == 'studio':
            studio.append(item.text)
        if item['href'][7:14] == 'country':
            country.append(item.text)
        if item['href'][7:15] == 'language':
            language.append(item.text)

    res['Country'] = country
    res['Studio'] = studio
    res['Language'] = language

    return res

def movie_description(movie: Movie) -> str:
    if type(movie) != Movie:
        raise Exception("Improper parameter")
        
    page = movie.get_parsed_page(movie.url)

    try:
        data = page.find_all("meta", attrs={'name':'twitter:description'})
        return data[0]['content']
    except:
        return None


def movie_poster(movie_id):
    '''Returns the poster link of a movie'''
    try:
        page = requests.get("https://letterboxd.com/film/" + movie_id + "/", timeout=5)
        page = BeautifulSoup(page.text, 'lxml')

        script_w_data = page.select_one('script[type="application/ld+json"]')
        link = json.loads(script_w_data.text.split(
            ' */')[1].split('/* ]]>')[0])['image']

    except AttributeError as exception:
        print(f'error on {movie_id}. Exception:' + str(exception))
        link = ''

    return link

class Encoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

if __name__ == "__main__":
    king = Movie("king kong")
    print(king)
    #king = Movie("king kong", 2005)
    #print(king)
    #house = Movie("/film/the-house-2022-1/")
    #print(house)
    #print(movie_popular_reviews(house))
