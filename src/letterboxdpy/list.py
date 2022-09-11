import json
import re
import requests
from bs4 import BeautifulSoup
from json import JSONEncoder

class List:
    def __init__(self, author: str, title: str) -> None:
        self.title = title.replace(' ', '-').lower()
        self.author = author.lower()
        self.url = "https://letterboxd.com/" + self.author +"/list/" + self.title + "/"

        page = self.get_parsed_page(self.url)
    
        self.description = self.description(page)
        self.filmCount = self.film_count(self.url)

    def jsonify(self) -> str:
        return json.dumps(self, indent=4,cls=Encoder)

    def get_parsed_page(self, url: str) -> None:
        # This fixes a blocked by cloudflare error i've encountered
        headers = {
            "referer": "https://letterboxd.com",
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

def list_tags(list: List) -> list:
    ret = []

    data = list.get_parsed_page(list.url)
    data = data.find("ul", {"class": ["tags"], })
    data = data.findChildren("a")

    for item in data:
        ret.append(item.text)

    return ret

class Encoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

if __name__ == "__main__":
    list = List("Horrorville", "The Official Top 25 Horror Films of 2022")
    print(list.jsonify())
    #print(list_tags(list))
