import json
import re
from datetime import datetime
from avatar import Avatar
from scraper import Scraper
from json import JSONEncoder


class User:
    DOMAIN = "https://letterboxd.com"
    MONTH_ABBREVIATIONS = [
        "Jan", "Feb", "Mar",
        "Apr", "May", "Jun",
        "Jul", "Aug", "Sep",
        "Oct", "Nov", "Dec"
        ]

    def __init__(self, username: str) -> None:
        assert re.match("^[A-Za-z0-9_]*$", username), "Invalid username"

        self.scraper = Scraper(self.DOMAIN)
        self.username = username.lower()
        self.url = f"{self.DOMAIN}/{self.username}"

        dom = self.scraper.get_parsed_page(self.url)

        self.user_details(dom)
        self.user_avatar(dom)
        self.user_recent(dom)

    def __str__(self):
        return self.jsonify()

    def jsonify(self) -> str:
        return json.dumps(self, indent=2, cls=Encoder)

    # letterboxd.com/?
    def user_avatar(self, dom) -> str:
        elem_avatar = dom.find("div", {"class": ["profile-avatar"]})
        avatar_url = elem_avatar.img['src']
        self.avatar = Avatar(avatar_url).upscaled_data

    # letterboxd.com/?
    def user_recent(self, dom) -> list:
        watchlist_recent = {}
        diary_recent = {'months':{}}

        # watchlist
        if self.watchlist_length:
            section_watchlist = dom.find("section", {"class": ["watchlist-aside"]})
            watchlist_items = section_watchlist.find_all("li", {"class": ["film-poster"]})
            for item in watchlist_items:
                watchlist_recent[item['data-film-id']] = {
                    'name': item.img['alt'],
                    'slug': item['data-film-slug'],
                }
        
        # diary
        sections = dom.find_all("section", {"class": ["section"]})
        for section in sections:
            if section.h2 is None:
                continue
    
            if section.h2.text == "Diary":
                entry_list = section.find_all("li", {"class": ["listitem"]})

                for entry in entry_list:
                    month = entry.h3.text
                    month_index = self.MONTH_ABBREVIATIONS.index(month) + 1
                    diary_recent['months'] |= {month_index: []}
                    days = entry.find_all("dt")
                    items = entry.find_all("dd")
                    for day, item in zip(days, items):
                        diary_recent['months'][month_index].append([day.text, item.text])
                else:
                    break

        data = {
            'watchlist': watchlist_recent,
            'diary': diary_recent
        }
        
        self.recent = data

    # letterboxd.com/?/
    def user_details(self, dom) -> dict:
        """
        methods:
        .id, .display_name, .bio, .location,
        .website, .watchlist_length, .stats, .favorites
        """

        # id
        """ alternative:
        button_report = page.find("button", {"data-js-trigger": ["report"]})
        self.id = int(button_report['data-report-url'].split(':')[-1].split('/')[0])
        """
        pattern = r"/ajax/person:(\d+)/report-for"
        self.id  = re.search(
            pattern,
            dom.prettify()
        ).group(1)

        # display name
        data = dom.find("meta", attrs={'property': 'og:title'})
        self.display_name = data['content'][:-10]

        # bio
        data = dom.find("meta", attrs={'property': 'og:description'})
        self.bio = data['content'].split('Bio: ')[-1] if data['content'].find('Bio: ') != -1 else None

        # location and website
        data = dom.find("div", {"class": ["profile-metadata"], })
        location = data.find("div", {"class": ["metadatum"], }) if data else None
        website = data.find("a") if data else None
        self.location = location.find("span").text if location else None
        self.website = website['href'] if website else None         

        # watchlist_length
        nav_links = dom.find_all("a", {"class": ["navlink"]})
        for link in nav_links:
            if "Watchlist" in link.text:
               if "rel" in link.attrs:
                    # 'User watchlist is not visible'
                    self.watchlist_length = None # feature: PrivateData(Exception)
                    break
               else:
                    # 'User watchlist is visible'
                    widget = dom.find("section", {"class": ["watchlist-aside"]})
                    self.watchlist_length = int(
                        widget.find("a", {"class": ["all-link"]}).text.replace(',','')
                        ) if widget else 0
                    break
            else:
                # hq members
                self.watchlist_length = None

        # stats
        stats = dom.find_all("h4", {"class": ["profile-statistic"], })
        self.stats = {} if stats else None
        for stat in stats:
            value = stat.span.text
            key = stat.text.lower().replace(value,'').replace(' ','_')
            self.stats[key]= int(value.replace(',',''))

        # favorites
        data = dom.find("section", {"id": ["favourites"], })
        data = data.findChildren("div") if data else []
        self.favorites = []
        for div in data:
            poster = div.find("img")
            self.favorites.append((
                poster['alt'], # movie name
                poster.parent['data-film-slug'] # movie slug
                ))
    
# letterboxd.com/?/films/
def user_films(user: User) -> dict:
    assert isinstance(user, User), "Improper parameter: user must be an instance of User."

    FILMS_PER_PAGE = 12*6
    count = 0
    rating_count = 0
    liked_count = 0
    movie_list = {'movies': {}}

    while True:
        count += 1
        dom = user.scraper.get_parsed_page(f"{user.url}/films/page/{count}/")

        poster_containers = dom.find_all("li", {"class": ["poster-container"], })

        for poster_container in poster_containers:
            poster = poster_container.div
            poster_viewingdata = poster_container.p
            rating = None
            liked = False
            if poster_viewingdata.span:
                for span in poster_viewingdata.find_all("span"):
                    if 'rating' in span['class']:
                        # ['rating', '-tiny', '-darker', 'rated-9']
                        rating = int(poster_viewingdata.span['class'][-1].split('-')[-1])
                        rating_count += 1
                    elif 'like' in span['class']:
                        # ['like', 'has-icon', 'icon-liked', 'icon-16']
                        liked = True
                        liked_count += 1

            movie_list["movies"][poster["data-film-slug"]] = {
                    'name': poster.img["alt"],
                    "id": poster["data-film-id"],
                    "rating": rating,
                    "liked": liked
                }

        if len(poster_containers) < FILMS_PER_PAGE:
            movie_list['count'] = len(movie_list['movies'])
            movie_list['liked_count'] = liked_count
            movie_list['rating_count'] = rating_count
            if liked_count:
                movie_list['liked_percentage'] = round(liked_count / movie_list['count'] * 100, 2)
            else:
                movie_list['liked_percentage'] = 0.0
            movie_list['rating_percentage'] = 0.0
            movie_list['rating_average'] = 0.0

            if rating_count:
                ratings = [movie['rating'] for movie in movie_list['movies'].values() if movie['rating'] is not None]
                movie_list['rating_percentage'] = round(rating_count / movie_list['count'] * 100, 2)
                movie_list['rating_average'] = round(sum(ratings) / rating_count, 2)

            break

    return movie_list

# letterboxd.com/?/following/
def user_following(user: User) -> dict:
    if type(user) != User:
        raise Exception("Improper parameter")

    # returns the first page of following
    dom = user.scraper.get_parsed_page(f"{user.url}/following/")
    data = dom.find_all("img", attrs={'height': '40'})

    ret = {}

    for person in data:
        ret[person.parent['href'].replace('/', '')] = {
            'display_name': person['alt'],
        }

    return ret

# letterboxd.com/?/followers/
def user_followers(user: User) -> dict:
    if type(user) != User:
        raise Exception("Improper parameter")

    #returns the first page of followers
    dom = user.scraper.get_parsed_page(f"{user.url}/followers/")
    data = dom.find_all("img", attrs={'height': '40'})

    ret = {}

    for person in data:
        ret[person.parent['href'].replace('/', '')] = {
            'display_name': person['alt'],
        }

    return ret

# letterboxd.com/?/films/genre/*/
def user_genre_info(user: User) -> dict:
    assert isinstance(user, User), "Improper parameter: user must be an instance of User."

    genres = ["action", "adventure", "animation", "comedy", "crime", "documentary",
              "drama", "family", "fantasy", "history", "horror", "music", "mystery",
              "romance", "science-fiction", "thriller", "tv-movie", "war", "western"]
    ret = {}
    for genre in genres:
        dom = user.scraper.get_parsed_page(f"{user.url}/films/genre/{genre}/")
        data = dom.find("span", {"class": ["replace-if-you"], })
        data = data.next_sibling.replace(',', '')
        try:
            ret[genre] = [int(s) for s in data.split() if s.isdigit()][0]
        except IndexError:
            ret[genre] = 0

    return ret

# letterboxd.com/?/films/reviews/
def user_reviews(user: User) -> dict:
    '''
    Returns a dictionary containing user reviews. The keys are unique log IDs,
    and each value is a dictionary with details about the review,
    including movie information, review type, rating, review content, date, etc.
    '''
    assert isinstance(user, User), "Improper parameter: user must be an instance of User."
    
    LOGS_PER_PAGE = 12

    page = 0
    data = {'reviews': {}}
    while True:
        page += 1
        dom = user.scraper.get_parsed_page(f"{user.url}/films/reviews/page/{page}/")
        logs = dom.find_all("li", {"class": ["film-detail"], })

        for log in logs:
            details = log.find("div", {"class": ["film-detail-content"], })

            movie_name = details.a.text
            slug = details.parent.div['data-film-slug']
            movie_id = details.parent.div['data-film-id']
            # str   ^^^--- movie_id: unique id of the movie.
            release = int(details.small.text) if details.small else None
            movie_link = f"{user.DOMAIN}/film/{slug}/"
            log_id = log['data-object-id'].split(':')[-1]
            # str ^^^--- log_id: unique id of the review.
            log_link = user.DOMAIN + details.a['href']
            log_no = log_link.split(slug)[-1]
            log_no = int(log_no.replace('/', '')) if log_no.count('/') == 2 else 0
            # int ^^^--- log_no: there can be multiple reviews for a movie.
            #            counting starts from zero.
            #            example for first review:  /username/film/movie_name/
            #            example for first review:  /username/film/movie_name/0/
            #            example for second review: /username/film/movie_name/1/
            #                the number is specified at the end of the url ---^
            rating = details.find("span", {"class": ["rating"], })
            rating = int(rating['class'][-1].split('-')[-1]) if rating else None
            # int ^^^--- rating: the numerical value of the rating given in the review (1-10)
            review = details.find("div", {"class": ["body-text"], })
            spoiler = bool(review.find("p", {"class": ["contains-spoilers"], }))
            # bool ^^^--- spoiler: whether the review contains spoiler warnings
            review = review.find_all('p')[1 if spoiler else 0:]
            review = '\n'.join([p.text for p in review])
            # str ^^^--- review: the text content of the review.
            #            spoiler warning is checked to include or exclude the first paragraph.
            date = details.find("span", {"class": ["_nobr"], })
            log_type = date.previous_sibling.text.strip()
            # str   ^^^--- log_type: Types of logs, such as:
            #              'Rewatched': (in diary) review, watched and rewatched 
            #              'Watched':   (in diary) review and watched
            #              'Added': (not in diary) review 
            if log_type == 'Added':
                # 2024-01-01T05:45:00.268Z
                date = dict(zip(
                    ['year', 'month', 'day'],
                    map(int, date.time['datetime'][:10].split('-')
                    )))
            else:
                # 01 Jan 2024
                date = date.text.split()
                date = {
                    'year': int(date[2]),
                    'month': user.MONTH_ABBREVIATIONS.index(date[1]) + 1,
                    'day': int(date[0])
                }
            # dict ^^^--- date: the date of the review.
            #             example: {'year': 2024, 'month': 1, 'day': 1}

            data['reviews'][log_id] = {
                # static
                'movie': {
                    'name': movie_name,
                    'slug': slug,
                    'id': movie_id,
                    'release': release,
                    'link': movie_link,
                },
                # dynamic
                'type': log_type,
                'no': log_no,
                'link': log_link,
                'rating': rating,
                'review': {
                    'content': review,
                    'spoiler': spoiler
                },
                'date': date,
                'page': page,
            }

        if len(logs) < LOGS_PER_PAGE:
            data['count'] = len(data['reviews'])
            data['last_page'] = page
            break

    return data

# letterboxd.com/?/films/diary/
def user_diary(user: User, year: int=None, page: int=None) -> dict:
    '''
    Returns:
      Returns a list of dictionaries with the user's diary'
      Each entry is represented as a dictionary with details such as movie name,
      release information,rewatch status, rating, like status, review status,
      and the date of the entry.
    '''
    assert isinstance(user, User), "Improper parameter: user must be an instance of User."
    
    BASE_URL = f"{user.url}/films/diary/{f'for/{year}/'*bool(year)}"
    pagination = page if page else 1
    ret = {'entrys': {}}

    while True:
        url = BASE_URL + f"page/{pagination}/"

        dom = user.scraper.get_parsed_page(url)
        table = dom.find("table", {"id": ["diary-table"], })

        if table:
            # extract the headers class of the table to use as keys for the entries
            # ['month','day','film','released','rating','like','rewatch','review', actions']
            headers = [elem['class'][0].split('-')[-1] for elem in table.find_all("th")]
            rows = dom.tbody.find_all("tr")

            for row in rows:
                # create a dictionary by mapping headers class
                # to corresponding columns in the row
                cols = dict(zip(headers, row.find_all('td')))

                # <tr class="diary-entry-row .." data-viewing-id="516951060" ..>
                log_id = row["data-viewing-id"]

                # day column
                date = dict(zip(
                        ["year", "month", "day"],
                        map(int, cols['day'].a['href'].split('/')[-4:])
                    ))
                # film column
                poster = cols['film'].div
                name = poster.img["alt"] or row.h3.text
                slug = poster["data-film-slug"]
                id = poster["data-film-id"]
                # released column
                release = cols["released"].text
                release = int(release) if len(release) else None
                # rewatch column
                rewatched = "icon-status-off" not in cols["rewatch"]["class"]
                # rating column
                rating = cols["rating"].span
                is_rating = 'rated-' in ''.join(rating["class"])
                rating = int(rating["class"][-1].split("-")[-1]) if is_rating else None
                # like column
                liked = bool(cols["like"].find("span", attrs={"class": "icon-liked"}))
                # review column
                reviewed = bool(cols["review"].a)
                # actions column
                actions = cols["actions"]
                """
                id = actions["data-film-id"] # !film col
                name = actions["data-film-name"] !# film col
                slug = actions["data-film-slug"] # !film col
                release = actions["ddata-film-release-year"] # !released col
                """
                runtime = actions["data-film-run-time"]
                runtime = int(runtime) if runtime else None

                # create entry
                ret["entrys"][log_id] = {
                    "name": name,
                    "slug": slug,
                    "id":  id,
                    "release": release,
                    "runtime": runtime,
                    "actions": {
                        "rewatched": rewatched,
                        "rating": rating,
                        "liked": liked,
                        "reviewed": reviewed,
                    },
                    "date": date,
                    "page": {
                        'url': url,
                        'no': pagination
                        }
                }
            if len(rows) < 50 or pagination == page:
                    # no more entries
                    # or reached the requested page
                    break
            pagination += 1
        else: # no table
            break

    ret['count'] = len(ret['entrys'])
    ret['last_page'] = pagination

    return ret

# dependency: user_diary()
def user_wrapped(user: User, year: int=2024) -> dict:

    assert isinstance(user, User), "Improper parameter: user must be an instance of User."

    diary = user_diary(user, year)

    movies = {}
    milestones = {}
    months = {}.fromkeys([1,2,3,4,5,6,7,8,9,10,11,12], 0)
    days = {}.fromkeys([1,2,3,4,5,6,7], 0)
    total_review = 0
    total_runtime = 0
    first_watched = None
    last_watched = None

    no = 0
    for log_id, data in diary['entrys'].items():
        watched_date = data['date']

        if watched_date['year'] == year:
            no += 1

            movies[log_id] = data

            days[datetime(**watched_date).weekday()+1] += 1
            months[watched_date['month']] += 1

            reviewed = data["actions"]['reviewed']
            total_review += 1 if reviewed else 0

            runtime = data['runtime']
            total_runtime += runtime if runtime else 0

            if not no % 50:
                milestones[no] = {log_id:data}

            if not last_watched:
                # first item is last watched
                last_watched = {log_id:data}
            else:
                # last item is first watched
                first_watched = {log_id:data}
    
    wrapped = {
        'year': year,
        'logged': len(movies),
        'total_review': total_review,
        'hours_watched': total_runtime // 60,
        'total_runtime': total_runtime,
        'first_watched': first_watched,
        'last_watched': last_watched,
        'movies': movies,
        'months': months,
        'days': days,
        'milestones': milestones
    }

    return wrapped

# letterboxd.com/?/activity
# letterboxd.com/ajax/activity-pagination/?/
def user_activity(user: User) -> dict:
    assert isinstance(user, User), "Improper parameter: user must be an instance of User."

    BASE_URL = f"{user.DOMAIN}/ajax/activity-pagination/{user.username}"
    data = {'user': user.username, 'logs': {}}
    url = BASE_URL

    dom = user.scraper.get_parsed_page(url)
    sections = dom.find_all("section")
    if not sections:
        print(f"User {user.username} has no activity.")
        return data

    for section in sections:
        
        log_id = None
        event_type = None

        if any(x.startswith('-') for x in section['class']):
            event_type = list(filter(lambda x: x.startswith('-'), section['class']))[0][1:]

        if event_type == 'review' or event_type == 'basic':
            log_id = section["data-activity-id"]
            data['logs'][log_id] = {}
            # event time
            date = section.find("time")
            date = datetime.strptime(date['datetime'], '%Y-%m-%dT%H:%M:%S.%fZ')
            data['logs'][log_id] |= {
                'event_type': event_type,
                'time': {
                    'year': date.year,
                    'month': date.month,
                    'day': date.day,
                    'hour': date.hour,
                    'minute': date.minute,
                    'second': date.second
                }
            }

            if event_type == 'review':
                # film
                detail = section.find("div", {"class": "film-detail-content"})
                log_title = detail.p.text.strip()
                log_type = log_title.split()[-1]
                film = detail.h2.find(text=True)
                # rating
                rating = section.find("span", {"class": ["rating"], })
                rating = int(rating['class'][-1].split('-')[-1]) if rating else None
                # year
                film_year = detail.h2.small.text
                film_year = int(film_year) if film_year else None
                # review
                review = detail.find("div", {"class": ["body-text"], })
                spoiler = bool(review.find("p", {"class": ["contains-spoilers"], }))
                review = review.find_all('p')[1 if spoiler else 0:]
                review = '\n'.join([p.text for p in review])
                data['logs'][log_id]|= {
                    'event': event_type,
                    'type': log_type,
                    'title': log_title,
                    'film': film,
                    'film_year': film_year,
                    'rating': rating,
                    'spoiler': spoiler,
                    'review': review
                }
            elif event_type == 'basic':
                log_title = section.p.text.strip()
                log_type = log_title.split()[1]
                data['logs'][log_id] |= {
                    'log_type': log_type,
                    'title': log_title
                    }

                # specials
                if log_type == 'followed':
                    username = section.find("a",{"class":["target"]})['href'].replace('/','')
                    data['logs'][log_id] |= {'username': username}
                elif log_type == 'liked':
                    # display name
                    # display_name = section.find("strong",{"class":["name"]}).text.replace('\u2019s',"")
                    username = section.find("a",{"class":["target"]})['href'].split('/')[1]
                    data['logs'][log_id] |= {'username': username}
                elif log_type == 'watched':
                    film = section.find("a",{"class":["target"]}).text.split('  ')[-1].strip()
                    film  = film if film else None
                    data['logs'][log_id] |= {'film': film}

        elif 'no-activity-message' in section['class']:
            break

    return data

# https://letterboxd.com/?/lists/
def user_lists(user: User) -> dict:
    assert isinstance(user, User), "Improper parameter: user must be an instance of User."

    BASE_URL = f"{user.url}/lists/"
    LISTS_PER_PAGE = 12

    selectors = {
        'list_set': ('section', {'class': 'list-set', }),
        'lists': ('section', {'class': 'list', }),
        'title': ('h2', {'class': 'title', }),
        'description': ('div', {'class': 'body-text', }),
        'value': ('small', {'class': 'value', }),
        'likes': ('a', {'class': 'icon-like', }),
        'comments': ('a', {'class': 'icon-comment', }),
    }

    page = 0
    data = {'lists': {}}
    while True:
        page += 1
        dom = user.scraper.get_parsed_page(f'{BASE_URL}/page/{page}')

        list_set = dom.find(*selectors['list_set'])
        if not list_set:
            break
        lists = list_set.find_all(*selectors['lists'])

        for item in lists:
            # id
            list_id = item['data-film-list-id']
            # title
            list_title = item.find(*selectors['title']).text.strip()
            # description
            description = item.find(*selectors['description'])
            if description:
                description = description.find_all('p')
                description = '\n'.join([p.text for p in description])
            # url
            list_url = item.find(*selectors['title']).a['href']
            # slug
            list_slug = list_url.split('/')[-2]
            # count
            count = int(item.find(*selectors['value']).text.split()[0].replace(',',''))
            # likes
            likes = item.find(*selectors['likes'])
            likes = likes if likes else 0
            if likes:
                likes = likes.text.split()[0].replace(',','')
                if 'K' in likes:
                    likes = likes.replace('K', '')
                    likes = float(likes) * 1000
                likes = int(likes)
            # comments
            # feature: https://letterboxd.com/ajax/filmlist:<list-id>/comments/
            comments = item.find(*selectors['comments'])
            comments = int(comments.text.split()[0].replace(',','')) if comments else 0

            data['lists'][list_id] = {
                'title': list_title,
                'slug': list_slug,
                'description': description,
                'url': user.DOMAIN + list_url,
                'count': count,
                'likes': likes,
                'comments': comments
                }

        if len(lists) < LISTS_PER_PAGE:
            break

    data['count'] = len(data['lists'])
    data['last_page'] = page
    return data

# https://letterboxd.com/?/watchlist/
def user_watchlist(user: User, filters: dict=None) -> dict:
    """
    filter examples:
        - keys: decade, year, genre

        # positive genre & negative genre (start with '-')
        - {genre: ['mystery']}  <- same -> {genre: 'mystery'}
        - {genre: ['-mystery']} <- same -> {genre: '-mystery'}

        # multiple genres
        - {genre: ['mystery', 'comedy'], decade: '1990s'}
        - {genre: ['mystery', '-comedy'], year: '2019'}
        - /decade/1990s/genre/action+-drama/
          ^^---> {'decade':'1990s','genre':['action','-drama']}
    """
    assert isinstance(user, User), "Improper parameter: user must be an instance of User."

    data = {
        'available': None,
        'count': user.watchlist_length,
        'data_count': None,
        'last_page': None,
        'filters': filters,
        'data': {}
        }

    if user.watchlist_length is None:
        # user watchlist is private
        return data | {'available': False}
    elif user.watchlist_length == 0:
        # user watchlist is empty
        return data | {'available': True}

    FILMS_PER_PAGE = 7*4
    BASE_URL = f"{user.url}/watchlist/"

    if filters and isinstance(filters, dict):
        f = ""
        for key, values in filters.items():
            if not isinstance(values, list):
                values = [values]
            f += f"{key}/"
            f += "+".join([str(v) for v in values]) + "/"

        BASE_URL += f

    page = 1
    no = user.watchlist_length
    while True:
        dom = user.scraper.get_parsed_page(f'{BASE_URL}/page/{page}')

        poster_containers = dom.find_all("li", {"class": ["poster-container"], })
        for poster_container in poster_containers:
            poster = poster_container.div
            img = poster_container.div.img

            film_id = poster['data-film-id']
            slug = poster['data-film-slug']
            name = img['alt']

            data['data'][film_id] = {
                'name': name,
                'slug': slug,
                'no': no,
                'page': page,
                'url': f"{user.DOMAIN}/films/{slug}/",
            }

            no -= 1

        if len(poster_containers) < FILMS_PER_PAGE:
            # last page
            break
        page += 1

    data_count = len(data['data'])

    if filters:
        if data_count != data['count']:
            no = data_count
            for item in data['data'].keys():
                data['data'][item]['no'] = no
                no -= 1

    data = data | {
        'available': True,
        'data_count': data_count,
        'last_page': page,
        }

    return data

# https://letterboxd.com/?/tags/*
def user_tags(user: User) -> dict:
    assert isinstance(user, User), "Improper parameter: user must be an instance of User."

    BASE_URL = f"{user.url}/tags/"

    pages = ['films', 'diary', 'reviews', 'lists']
    data = {page: {'tags': {}, 'count': 0} for page in pages}

    for page in pages:
        dom = user.scraper.get_parsed_page(BASE_URL + page)
        tags_columns = dom.find("ul", {"class": ["tags-columns"]})

        if not tags_columns:
            continue

        tags = tags_columns.find_all("li")

        no = 0
        for tag in tags:
            if 'href' in tag.a.attrs:
                no += 1
                name = tag.a.text.strip()
                title = tag.a['title']
                link = tag.a['href']
                slug = link.split('/')[-3]
                count = tag.span.text.strip()
                count = int(count) if count else 1

                data[page]['tags'][slug] = {
                    'name': name,
                    'title': title,
                    'link': link,
                    'count': count,
                    'no': no
                    }
            else:
                pass # not a tag

        data[page]['count'] = no
    data['count'] = sum([data[page]['count'] for page in pages])

    return data

class Encoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

if __name__ == "__main__":
    import argparse
    import sys

    # Reconfigure stdout encoding to UTF-8 to support non-ASCII characters
    sys.stdout.reconfigure(encoding='utf-8')

    # Parse command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--user', dest="user", help="Username to gather stats on")
    args = parser.parse_args()

    # Extract username from command-line arguments or prompt user for input
    username = args.user or ''

    # Keep prompting user until a valid username is provided
    while not len(username.strip()):
        username = input('Enter username: ')

    # Display the username being processed
    print(f"Processing username: {username}")

    # Initialize a User instance with the provided username
    user_instance = User(username.lower())

    # Print user statistics
    print(user_instance)

    # Iterate over user's film data and print each movie
    for item in user_films(user_instance)['movies'].items():
        print(item)