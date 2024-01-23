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


def user_films_watched(user: User) -> dict:
    assert isinstance(user, User), "Improper parameter: user must be an instance of User."

    #returns all movies
    count = 0
    rating_count = 0
    liked_count = 0
    movie_list = {'movies': {}}

    while True:
        count += 1
        page = user.get_parsed_page("https://letterboxd.com/" + user.username + "/films/page/" + str(count) + "/")

        poster_containers = page.find_all("li", {"class": ["poster-container"], })
        for poster_container in poster_containers:
            poster = poster_container.div
            poster_viewingdata = poster_container.p

            if '-rated-and-liked' in poster_viewingdata['class']:
                rating = int(poster_viewingdata.span['class'][-1].split('-')[-1])
                liked = True
                liked_count += 1
                rating_count += 1
            else:
                rating = None
                liked = False
                if poster_viewingdata.span:
                    if 'rating' in poster_viewingdata.span['class']:
                        # ['rating', '-tiny', '-darker', 'rated-9']
                        rating = int(poster_viewingdata.span['class'][-1].split('-')[-1])
                        rating_count += 1
                    elif 'like' in poster_viewingdata.span['class']:
                        # ['like', 'has-icon', 'icon-liked', 'icon-16']
                        liked = True
                        liked_count += 1

            movie_list["movies"][poster["data-film-slug"]] = {
                    'name': poster.img["alt"],
                    "id": poster["data-film-id"],
                    "rating": rating,
                    "liked": liked
                }

        if len(poster_containers) < 72:
            movie_list['count'] = len(movie_list['movies'])
            movie_list['liked_count'] = liked_count
            movie_list['rating_count'] = rating_count
            movie_list['liked_percentage'] = round(liked_count / movie_list['count'] * 100, 2)
            movie_list['rating_percentage'] = 0.0
            movie_list['rating_average'] = 0.0

            if rating_count:
                ratings = [movie['rating'] for movie in movie_list['movies'].values() if movie['rating'] is not None]
                movie_list['rating_percentage'] = round(rating_count / movie_list['count'] * 100, 2)
                movie_list['rating_average'] = round(sum(ratings) / rating_count, 2)

            break

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


def user_following(user: User) -> dict:
    if type(user) != User:
        raise Exception("Improper parameter")

    # returns the first page of following
    page = user.get_parsed_page("https://letterboxd.com/" + user.username + "/following/")
    data = page.find_all("img", attrs={'height': '40'})

    ret = {}

    for person in data:
        ret[person.parent['href'].replace('/', '')] = {
            'display_name': person['alt'],
        }

    return ret


def user_followers(user: User) -> dict:
    if type(user) != User:
        raise Exception("Improper parameter")

    #returns the first page of followers
    page = user.get_parsed_page("https://letterboxd.com/" + user.username + "/followers/")
    data = page.find_all("img", attrs={'height': '40'})

    ret = {}

    for person in data:
        ret[person.parent['href'].replace('/', '')] = {
            'display_name': person['alt'],
        }

    return ret


def user_genre_info(user: User) -> dict:
    assert isinstance(user, User), "Improper parameter: user must be an instance of User."

    genres = ["action", "adventure", "animation", "comedy", "crime", "documentary",
              "drama", "family", "fantasy", "history", "horror", "music", "mystery",
              "romance", "science-fiction", "thriller", "tv-movie", "war", "western"]
    ret = {}
    for genre in genres:
        page = user.get_parsed_page("https://letterboxd.com/" + user.username + 
                                    "/films/genre/" + genre + "/")
        data = page.find("span", {"class": ["replace-if-you"], })
        data = data.next_sibling.replace(',', '')
        ret[genre] = [int(s) for s in data.split() if s.isdigit()][0]
        
    return ret


#gives reviews that the user selected has made
def user_reviews(user: User) -> dict:
    assert isinstance(user, User), "Improper parameter: user must be an instance of User."

    paginate = 0
    data = {'reviews': {}}
    while True:
        paginate += 1
        page = user.get_parsed_page(f"https://letterboxd.com/{user.username}/films/reviews/page/{paginate}/")

        contents = page.find_all("div", {"class": ["film-detail-content"], })

        for item in contents:
            rating = item.find("span", {"class": ["rating"], })

            data['reviews'][item.parent.div['data-film-slug']] = {
                'movie': item.a.text,
                'movie_id': item.parent.div['data-film-id'],
                'movie_year': int(item.small.text) if item.small else None,
                'rating': int(rating['class'][-1].split('-')[-1]) if rating else None,
                'review': item.find("div", {"class": ["body-text"], }).findChildren()[0].text,
                'date': item.find("span", {"class": ["_nobr"], }).text
            }

        if len(contents) < 12:
            data['count'] = len(data['reviews'])
            data['last_page'] = paginate
            break

    return data


def user_diary_page(user: User, page:int=1) -> dict:
    '''
    Returns the user's diary entries for a specific page.

    Returns:
    - dict: A dictionary containing diary entries for the specified page.
      Each entry is represented as a dictionary with details such as movie name,
      release information,rewatch status, rating, like status, review status,
      and the date of the entry.
    '''
    assert isinstance(user, User), "Improper parameter: user must be an instance of User."

    dom = user.get_parsed_page(
        f"https://letterboxd.com/{user.username}/films/diary/page/{page}/")

    ret = {'entrys': {}}

    table = dom.find("table", {"id": ["diary-table"], })

    if table:
        # extract the headers of the table to use as keys for the entries
        headers = [elem.text.lower() for elem in table.find_all("th")]
        rows = dom.tbody.find_all("tr")

        for row in rows:
            # create a dictionary by mapping headers
            # to corresponding columns in the row
            cols = dict(zip(headers, row.find_all('td')))

            poster = cols['film'].div
            rating = cols["rating"].span
            release = cols["released"].text

            log_id = row["data-viewing-id"]
            date = dict(zip(
                    ["year", "month", "day"],
                    map(int, cols['day'].a['href'].split('/')[-4:])
                ))
            name = poster.img["alt"] or row.h3.text
            slug = poster["data-film-slug"]
            id = poster["data-film-id"]
            release = int(release) if len(release) else None
            rewatched = "icon-status-off" not in cols["rewatch"]["class"]
            is_rating = 'rated-' in ''.join(rating["class"])
            rating = int(rating["class"][-1].split("-")[-1]) if is_rating else None
            liked = bool(cols["like"].find("span", attrs={"class": "icon-liked"}))
            reviewed = bool(cols["review"].a)

            ret["entrys"][log_id] = {
                "name": name,
                "slug": slug,
                "id":  id,
                "release": release,
                "rewatched": rewatched,
                "rating": rating,
                "liked": liked,
                "reviewed": reviewed,
                "date": date,
                "page": page,
            }

    return ret


def user_diary(user: User) -> dict:
    '''Returns a list of dictionaries with the user's diary'''
    assert isinstance(user, User), "Improper parameter: user must be an instance of User."
    
    ret = {'entrys': {}}
    pagination = 1
    while True:
        page_result = user_diary_page(user, pagination)
        entrys = page_result['entrys']
        ret['entrys'].update(entrys)
        if len(entrys) < 50:
            print(f"Last page: {pagination}")
            break
        pagination += 1

    ret['count'] = len(ret['entrys'])
    ret['last_page'] = pagination

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

