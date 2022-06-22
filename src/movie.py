import json
import re
import requests
from bs4 import BeautifulSoup
from json import JSONEncoder

class Movie:
    def __init__(self, title, year=''):
        if not self.check_year(title, year):
            year = ''
        self.title = title
        self.director = self.movie_director(title, year)
        self.rating = self.movie_rating(title, year)
        self.description = self.movie_description(title, year)
        self.year = self.movie_year(title, year)

    def jsonify(self):
        return json.dumps(self, indent=4,cls=Encoder)

    def get_parsed_page(self, url):
        # This fixes a blocked by cloudflare error i've encountered
        headers = {
            "referer": "https://liquipedia.net/rocketleague/Portal:Statistics",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }

        return BeautifulSoup(requests.get(url, headers=headers).text, "lxml")

    def movie_director(self, movie, year):
        if year != '':
            movie = movie + ' ' + str(year)
        movie = movie.replace(' ', '-')
        page = self.get_parsed_page("https://letterboxd.com/film/" + movie + "/")

        crew = page.find_all("span", text = 'Director')
        if len(crew) != 0:
            director = crew[0].parent.parent.findChildren("a")
            director = director[0].text
        else:
            crew = page.find_all("span", text = 'Directors')
            directors = crew[0].parent.parent.findChildren("p")[0]
            directors = directors.findChildren("a")
            director = []
            for item in directors:
                director.append(item.text)
            
        return director

    def movie_rating(self, movie, year):
        if year != '':
            movie = movie + ' ' + str(year)
        movie = movie.replace(' ', '-')
        page = self.get_parsed_page("https://letterboxd.com/film/" + movie + "/")

        meta = page.find_all("meta", attrs={'name':'twitter:data2'})
        if len(meta) == 0:
            return meta
        content = meta[0]['content']

        return content

    def movie_description(self, movie, year):
        if year != '':
            movie = movie + ' ' + str(year)
        movie = movie.replace(' ', '-')
        page = self.get_parsed_page("https://letterboxd.com/film/" + movie + "/")

        meta = page.find_all("meta", attrs={'name':'twitter:description'})
        content = meta[0]['content']

        if "\u2026" in content:
            content = content.replace("\u2026", "...")

        return content

    def movie_year(self, movie, year):
        if year != '':
            movie = movie + ' ' + str(year)
        movie = movie.replace(' ', '-')
        page = self.get_parsed_page("https://letterboxd.com/film/" + movie + "/")

        meta = page.find_all("meta", attrs={'name': 'twitter:title'})[0]['content']
        true_year = meta[meta.find('(')+1:meta.find(')')]

        return true_year

    def check_year(self, movie, year):
        if year != '':
            movie = movie + ' ' + str(year)
        movie = movie.replace(' ', '-')
        page = self.get_parsed_page("https://letterboxd.com/film/" + movie + "/")

        meta = page.find_all("meta", attrs={'name': 'twitter:title'})[0]['content']
        true_year = meta[meta.find('(')+1:meta.find(')')]

        if str(true_year) != str(year) and year != '':
            return False
        return True

class Encoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

if __name__ == "__main__":
    king = Movie("house", 1975)
    print(king.jsonify())
