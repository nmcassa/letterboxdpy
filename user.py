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

class Encoder(JSONEncoder):
    def default(self, o):
        return o.__dict__
