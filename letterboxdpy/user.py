import json
from json import JSONEncoder
import re
import requests
from bs4 import BeautifulSoup


class User:
    def __init__(self, username: str) -> None:
        if not re.match("^[A-Za-z0-9_]*$", username):
            raise Exception("Invalid username")

        self.username = username.lower()

        page = self.get_parsed_page("https://letterboxd.com/" + self.username + "/")
        
        self.user_watchlist()
        self.user_favorites(page)
        self.user_stats(page)
    
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

    def user_favorites(self, page: None) -> list:        
        data = page.find("section", {"id": ["favourites"], }).findChildren("div")
        names = []

        for div in data:
            img = div.find("img")
            movie_url = img.parent['data-film-slug']
            names.append((img['alt'], movie_url))
            
        self.favorites = names

    def user_stats(self, page: None) -> dict:
        span = []
        stats = {}

        data = page.find_all("h4", {"class": ["profile-statistic"], })

        for item in data:
            span.append(item.findChildren("span"))

        for item in span:
            stats[item[1].text.replace(u'\xa0', ' ')] = item[0].text

        self.stats = stats

    def user_watchlist(self) -> str:
        page = self.get_parsed_page("https://letterboxd.com/" + self.username + "/watchlist/")
        data = page.find("span", {"class": ["watchlist-count"], })
        if not data:
            data = page.find("span", {"class": ["js-watchlist-count"], })
        try:
            ret = data.text.split('\xa0')[0] #remove 'films' from '76 films'
        except:
            raise Exception("No user found")

        self.watchlist_length = ret


def user_films_watched(user: User) -> list:
    if type(user) != User:
        raise Exception("Improper parameter")

    #returns all movies
    prev = count = 0
    curr = 1
    movie_list = []

    while prev != curr:
        count += 1
        prev = len(movie_list)
        page = user.get_parsed_page("https://letterboxd.com/" + user.username + "/films/page/" + str(count) + "/")

        img = page.find_all("img", {"class": ["image"], })

        for item in img:
            movie_url = item.parent['data-film-slug']
            movie_list.append((item['alt'], movie_url))

        curr = len(movie_list)
            
    return movie_list


def user_films_rated(user: User) -> list:
    """ """
    if type(user) != User:
        raise Exception("Improper parameter")

    prev = count = 0
    curr = -1
    rating_list = []

    while prev != curr:
        count += 1
        prev = len(rating_list)
        page = user.get_parsed_page("https://letterboxd.com/" + user.username + "/films/page/" + str(count) + "/")

        ps = page.find_all("p", {"class": ["poster-viewingdata"], })
        for p in ps:
            film_id = p.parent.div['data-film-id']
            film_url_pattern = p.parent.div['data-film-slug']
            rating = "NR"
            film_title_unreliable = ""
            try:
                film_title_unreliable = p.parent.img['alt']
            except Exception as e:
                print(f"[Error]: couldn't get film title. {e=}")

            try:
                spans = p.find_all('span')
                if spans:
                    rating = spans[0].text
            except Exception as e:
                print(f"[Error]: couldn't get film rating. {e=}")
            finally:
                rating_list.append( (film_title_unreliable, film_id, film_url_pattern, rating ) )

        curr = len(rating_list)

    return rating_list


def user_following(user: User) -> list:
    if type(user) != User:
        raise Exception("Improper parameter")

    # returns the first page of following
    page = user.get_parsed_page("https://letterboxd.com/" + user.username + "/following/")
    data = page.find_all("img", attrs={'height': '40'})

    ret = {}

    for person in data:
        ret[person.parent['href']] = person['alt']

    return ret


def user_followers(user: User) -> list:
    if type(user) != User:
        raise Exception("Improper parameter")

    #returns the first page of followers
    page = user.get_parsed_page("https://letterboxd.com/" + user.username + "/followers/")
    data = page.find_all("img", attrs={'height': '40'})

    ret = {}

    for person in data:
        ret[person.parent['href']] = person['alt']

    return ret


def user_genre_info(user: User) -> dict:
    if type(user) != User:
        raise Exception("Improper parameter")

    genres = ["action", "adventure", "animation", "comedy", "crime", "documentary",
              "drama", "family", "fantasy", "history", "horror", "music", "mystery",
              "romance", "science-fiction", "thriller", "tv-movie", "war", "western"]
    ret = {}
    for genre in genres:
        page = user.get_parsed_page("https://letterboxd.com/" + user.username +
                                    "/films/genre/" + genre + "/")
        data = page.find("span", {"class": ["replace-if-you"], })
        data = data.next_sibling
        ret[genre] = [int(s) for s in data.split() if s.isdigit()][0]
        
    return ret


#gives reviews that the user selected has made
def user_reviews(user: User) -> list:
    if type(user) != User:
        raise Exception("Improper parameter")

    page = user.get_parsed_page("https://letterboxd.com/" + user.username + "/films/reviews/")
    ret = []

    data = page.find_all("div", {"class": ["film-detail-content"], })

    for item in data:
        curr = {}

        curr['movie'] = item.find("a").text #movie title
        curr['rating'] = item.find("span", {"class": ["rating"], }).text #movie rating
        curr['date'] = item.find("span", {"class": ["_nobr"], }).text #rating date
        curr['review'] = item.find("div", {"class": ["body-text"], }).findChildren()[0].text #review

        ret.append(curr)

    return ret


def user_diary_page(user: User, page) -> list:
    '''Returns the user's diary for a specific page'''

    if type(user) != User:
        raise Exception("Improper parameter")

    page = user.get_parsed_page(
        "https://letterboxd.com/" + user.username + "/films/diary/page/"+str(page)+"/")
    ret = []

    data = page.find_all("tr", {"class": ["diary-entry-row"], })
    month_year = ''
    for item in data:
        curr = {}

        curr['movie'] = item.find("h3").text  # movie title
        curr['movie_id'] = item.find("h3").find('a')['href'].split('/')[3] # movie id
        curr['rating'] = item.find(
            "span", {"class": ["rating"], }).text.strip()  # movie rating
        day = item.find(
            "td", {"class": ["td-day diary-day center"], }).text  # rating date

        day = day.replace(' ', '').replace(' ', '')

        # Checks if the date is still in the same month. If not, it changes the month_year
        tmp_monthyear = item.find(
            "td", {"class": ["td-calendar"], }).text.replace(' ', '').replace(' ', '')

        if tmp_monthyear != '':
            month_year = item.find("td", {"class": ["td-calendar"], }).text

        curr['date'] = day.strip() + ' ' + month_year.strip()  # rating date
        ret.append(curr)

    return ret


def user_diary(user: User) -> list:
    '''Returns a list of dictionaries with the user's diary'''

    page = user.get_parsed_page(
        "https://letterboxd.com/" + user.username + "/films/diary/")

    # Get the max number of pages
    try:
        max_page = page.findAll("li", {"class": ["paginate-page"], })[-1].text
        print(max_page)
        ret = []

        for i in range(1, int(max_page)+1):
            page_result = user_diary_page(user, i)
            ret.extend(page_result)

    except IndexError:
        print('No diary found')
        ret =[]

    return ret


class Encoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--user', dest="user", help="Username to gather stats on")
    args = parser.parse_args()
    user = args.user

    if user:
        print(f"{user=}")
        userinfo = User(user)
        print(userinfo)
        # print(user_films_watched(userinfo))
        ratings = user_films_rated(userinfo)
        print(ratings)

