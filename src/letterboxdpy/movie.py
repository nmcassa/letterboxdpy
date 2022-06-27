import json
import re
import requests
from bs4 import BeautifulSoup
from json import JSONEncoder

class Movie:
    def __init__(self, title, year=''):
        if year != '':
            title = title + ' ' + str(year)
        title = title.replace(' ', '-')
        page = self.get_parsed_page("https://letterboxd.com/film/" + title + "/")

        if not self.check_year(title, year, page):
            year = ''
        
        self.title = title
        self.director = self.movie_director(title, year, page)
        self.rating = self.movie_rating(title, year, page)
        self.description = self.movie_description(title, year, page)
        self.year = self.movie_year(title, year, page)
        self.genres = self.movie_genre(title, year, page)
        self.details = self.movie_details(title, year)

    def jsonify(self):
        return json.dumps(self, indent=4,cls=Encoder)

    def get_parsed_page(self, url):
        # This fixes a blocked by cloudflare error i've encountered
        headers = {
            "referer": "https://liquipedia.net/rocketleague/Portal:Statistics",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }

        return BeautifulSoup(requests.get(url, headers=headers).text, "lxml")

    def movie_director(self, movie, year, page):
        crew = page.find_all("span", text = 'Director')
        if len(crew) != 0:
            director = crew[0].parent.parent.findChildren("a")
            director = director[0].text
        else:
            crew = page.find_all("span", text = 'Directors')
            if len(crew) == 0:
                return []
            directors = crew[0].parent.parent.findChildren("p")[0]
            directors = directors.findChildren("a")
            director = []
            for item in directors:
                director.append(item.text)
            
        return director

    def movie_rating(self, movie, year, page):
        meta = page.find_all("meta", attrs={'name':'twitter:data2'})
        if len(meta) == 0:
            return meta
        content = meta[0]['content']

        return content

    def movie_description(self, movie, year, page):
        meta = page.find_all("meta", attrs={'name':'twitter:description'})
        if len(meta) == 0:
            return ''
        content = meta[0]['content']

        if "\u2026" in content:
            content = content.replace("\u2026", "...")

        return content

    def movie_year(self, movie, year, page):
        meta = page.find_all("meta", attrs={'name': 'twitter:title'})
        if len(meta) == 0:
            return ""
        else :
            meta = meta[0]['content']
            true_year = meta[meta.find('(')+1:meta.find(')')]

        return true_year

    def check_year(self, movie, year, page):
        meta = page.find_all("meta", attrs={'name': 'twitter:title'})
        if len(meta) == 0:
            return True
        else :
            meta = meta[0]['content']
            true_year = meta[meta.find('(')+1:meta.find(')')]

        if str(true_year) != str(year) and year != '':
            return False
        return True

    def movie_genre(self, movie, year, page):
        res = []

        div = page.find_all("div",{"id": ["tab-genres"], })
        a = div[0].find_all("a")

        for item in a:
            if item['href'][7:12] == 'genre':
                res.append(item.text)

        return res

    def movie_details(self, movie, year):
        page = self.get_parsed_page("https://letterboxd.com/film/" + movie + "/details/")

        res = {}
        studio = []
        country = []
        language = []

        div = page.find_all("div", {"id": ["tab-details"], })
        a = div[0].find_all("a")

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
        

class Encoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

if __name__ == "__main__":
    king = Movie("king kong")
    print(king.jsonify())
    king = Movie("king kong", 2005)
    print(king.jsonify())
