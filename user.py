import json
from json import JSONEncoder
import re
import requests
from bs4 import BeautifulSoup

class User:
    def __init__(self, username):
        self.username = username
        self.favorites = self.user_favorites(username)
        self.stats = self.user_stats(username)
        self.watchlist_count = self.user_watchlist(username)
        #self.films = self.user_films_watched(username)
        self.following = self.user_following(username)
        self.followers = self.user_followers(username)

    def jsonify(self):
        return json.dumps(self, indent=4,cls=Encoder)

    def get_parsed_page(self, url):
        # This fixes a blocked by cloudflare error i've encountered
        headers = {
            "referer": "https://liquipedia.net/rocketleague/Portal:Statistics",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }

        return BeautifulSoup(requests.get(url, headers=headers).text, "lxml")

    def user_favorites(self, user):
        page = self.get_parsed_page("https://letterboxd.com/" + user + "/")
        
        section = page.find_all("section", {"id": ["favourites"], })
        movies = section[0].findChildren("div")
        names = []

        for div in movies:
            img = div.find("img")
            names.append(img['alt'])
            
        return names

    def user_stats(self, user):
        page = self.get_parsed_page("https://letterboxd.com/" + user + "/")
        span = []
        stats = {}

        header = page.find_all("h4", {"class": ["profile-statistic"], })

        for item in header:
            span.append(item.findChildren("span"))

        for item in span:
            stats[item[1].text.replace(u'\xa0', ' ')] = item[0].text

        return stats

    def user_watchlist(self, user):
        page = self.get_parsed_page("https://letterboxd.com/" + user + "/watchlist/")

        count = page.find_all("span", {"class": ["watchlist-count"], })

        ret = count[0].text.split('\xa0')

        return ret[0]

    def user_films_watched(self, user):
        #returns all movies
        prev = count = 0
        curr = 1
        movie_list = []
        while prev != curr:
            count += 1
            prev = len(movie_list)
            page = self.get_parsed_page("https://letterboxd.com/" + user + "/films/page/" + str(count) + "/")

            img = page.find_all("img", {"class": ["image"], })
            for alt in img:
                movie_list.append(alt['alt'])
            curr = len(movie_list)
            
        return movie_list

    def user_following(self, user):
        #returns the first page of following
        page = self.get_parsed_page("https://letterboxd.com/" + user + "/following/")
        img = page.find_all("img", attrs={'height': '40'})

        ret = []

        for person in img:
            ret.append(person['alt'])

        return ret

    def user_followers(self, user):
        #returns the first page of followers
        page = self.get_parsed_page("https://letterboxd.com/" + user + "/followers/")
        img = page.find_all("img", attrs={'height': '40'})

        ret = []

        for person in img:
            ret.append(person['alt'])

        return ret

class Encoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

if __name__ == "__main__":
    nick = User("connoreatspants")
    print(nick.jsonify())
