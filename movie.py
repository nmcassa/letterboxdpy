import json
import re
import requests
from bs4 import BeautifulSoup
from json import JSONEncoder

class Movie:
    def __init__(self, title):
        self.title = title
        self.director = self.movie_director(title)
        self.year = self.movie_year(title)
        self.rating = self.movie_rating(title)
        self.description = self.movie_description(title)

    def jsonify(self):
        return json.dumps(self, indent=4,cls=Encoder)

    def get_parsed_page(self, url):
        # This fixes a blocked by cloudflare error i've encountered
        headers = {
            "referer": "https://liquipedia.net/rocketleague/Portal:Statistics",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }

        return BeautifulSoup(requests.get(url, headers=headers).text, "lxml")

    def movie_director(self, movie):
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

    def movie_rating(self, movie):
        movie = movie.replace(' ', '-')
        page = self.get_parsed_page("https://letterboxd.com/film/" + movie + "/")

        meta = page.find_all("meta", attrs={'name':'twitter:data2'})
        content = meta[0]['content']

        return content

    def movie_description(self, movie):
        movie = movie.replace(' ', '-')
        page = self.get_parsed_page("https://letterboxd.com/film/" + movie + "/")

        meta = page.find_all("meta", attrs={'name':'twitter:description'})
        content = meta[0]['content']

        if "\u2026" in content:
            content = content.replace("\u2026", "...")

        return content

    def movie_year(self, movie):
        movie = movie.replace(' ', '-')
        page = self.get_parsed_page("https://letterboxd.com/film/" + movie + "/")

        meta = page.find_all("meta", attrs={'name': 'twitter:title'})[0]['content']

        return meta[meta.find('(')+1:meta.find(')')]

class Encoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

if __name__ == "__main__":
    king = Movie("the florida project")
    print(king.jsonify())
