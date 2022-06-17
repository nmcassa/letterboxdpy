import re
import requests
from bs4 import BeautifulSoup
from user import *

def get_parsed_page(url):
    # This fixes a blocked by cloudflare error i've encountered
    headers = {
        "referer": "https://liquipedia.net/rocketleague/Portal:Statistics",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    return BeautifulSoup(requests.get(url, headers=headers).text, "lxml")

def user_favorites(user):
    page = get_parsed_page("https://letterboxd.com/" + user + "/")
    
    section = page.find_all("section", {"id": ["favourites"], })
    movies = section[0].findChildren("div")
    names = []

    for div in movies:
        img = div.find("img")
        names.append(img['alt'])
        
    return names

def user_stats(user):
    page = get_parsed_page("https://letterboxd.com/" + user + "/")
    span = []
    stats = {}

    header = page.find_all("h4", {"class": ["profile-statistic"], })

    for item in header:
        span.append(item.findChildren("span"))

    for item in span:
        stats[item[1].text.replace(u'\xa0', ' ')] = item[0].text

    return stats

if __name__ == "__main__":
    import pprint
    pp = pprint.PrettyPrinter()

    print("My favorites from my account: \n")
    pp.pprint(user_favorites("nmcassa"))
    
    print("Stats from my account:\n")
    pp.pprint(user_stats("nmcassa"))

    nick = User("nmcassa", user_stats("nmcassa"))
    print("JSON of my User Object:\n")
    print(nick.jsonify())
    
