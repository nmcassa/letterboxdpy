import json
import re
import requests
from bs4 import BeautifulSoup
from json import JSONEncoder

class List:
    def __init__(self, url: str) -> None:
        page = self.get_parsed_page(url)
        
        self.title = self.list_title(page)
        self.author = self.author(page)
        self.description = self.description(page)
        self.filmCount = self.film_count(url)

    def jsonify(self) -> str:
        return json.dumps(self, indent=4,cls=Encoder)

    def get_parsed_page(self, url: str) -> None:
        # This fixes a blocked by cloudflare error i've encountered
        headers = {
            "referer": "https://liquipedia.net/rocketleague/Portal:Statistics",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }

        return BeautifulSoup(requests.get(url, headers=headers).text, "lxml")

    def list_title(self, page: None) -> str:
        data = page.find("meta", attrs={'property': 'og:title'})
        return data['content']

    def author(self, page: None) -> str:
        data = page.find("span", attrs={'itemprop': 'name'})
        return data.text

    def description(self, page: None) -> str:
        data = page.find_all("meta", attrs={'property': 'og:description'})
        if len(data) == 0:
            return ''
        return data[0]['content']

    def film_count(self, url: str) -> int: #and movie_list!!
        prev = count = 0
        curr = 1
        movie_list = []
        while prev != curr:
            count += 1
            prev = len(movie_list)
            page = self.get_parsed_page(url + "page/" + str(count) + "/")

            img = page.find_all("img", {"class": ["image"], })
            for alt in img:
                movie_list.append(alt['alt'])
            curr = len(movie_list)

        self.movies = movie_list
        return curr

class Encoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

if __name__ == "__main__":
        list = List("https://letterboxd.com/nmcassa/list/movies-for-sale-and-my-local-goodwill/")
        print(list.jsonify())
