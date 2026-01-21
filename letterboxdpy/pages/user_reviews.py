from letterboxdpy.core.scraper import parse_url
from letterboxdpy.utils.utils_parser import parse_review_date, parse_review_text
from letterboxdpy.constants.project import DOMAIN


class UserReviews:

    def __init__(self, username: str) -> None:
        self.username = username
        self.url = f"{DOMAIN}/{self.username}/films/reviews"
        
    def get_reviews(self): return extract_user_reviews(self.url)

def extract_user_reviews(url: str) -> dict:
    '''
    Returns a dictionary containing user reviews. The keys are unique log IDs,
    and each value is a dictionary with details about the review,
    including movie information, review type, rating, review content, date, etc.
    '''
    LOGS_PER_PAGE = 12

    page = 0
    data = {'reviews': {}}
    while True:
        page += 1
        dom = parse_url(f"{url.rstrip('/')}/page/{page}/")

        container = dom.find("div", {"class": ["viewing-list"]})

        if not container:
            # No container (div.viewing-list) found in the page.
            ...

        logs = container.find_all("article")

        if not logs:
            # No item (article) found in container.
            ...

        for log in logs:
            # Handle react structure
            react_component = log.parent.find("div", {"class": "react-component"}) or log.parent.div
            
            movie_name = log.a.text
            slug = react_component.get('data-item-slug') or react_component.get('data-film-slug')
            movie_id = react_component['data-film-id']
            # str   ^^^--- movie_id: unique id of the movie.
            # Find release year in spans
            release = None
            spans = log.find_all('span')
            for span in spans:
                if span.text and span.text.strip().isdigit() and len(span.text.strip()) == 4:
                    release = int(span.text.strip())
                    break
            movie_link = f"{DOMAIN}/film/{slug}/"
            log_id = log['data-object-id'].split(':')[-1]
            # str ^^^--- log_id: unique id of the review.
            log_link = DOMAIN + log.a['href']
            log_no = log_link.split(slug)[-1]
            log_no = int(log_no.replace('/', '')) if log_no.count('/') == 2 else 0
            # int ^^^--- log_no: there can be multiple reviews for a movie.
            #            counting starts from zero.
            #            example for first review:  /username/film/movie_name/
            #            example for first review:  /username/film/movie_name/0/
            #            example for second review: /username/film/movie_name/1/
            #                the number is specified at the end of the url ---^
            rating = log.find("span", {"class": ["rating"], })
            rating = int(rating['class'][-1].split('-')[-1]) if rating else None
            # int ^^^--- rating: the numerical value of the rating given in the review (1-10)
            review, spoiler = parse_review_text(log)
            # str ^^^--- review: the text content of the review.
            #            spoiler warning is checked to include or exclude the first paragraph.
            date = log.find("span", {"class": ["date"], })
            log_type = date.find_previous_sibling().text.strip()
            # str   ^^^--- log_type: Types of logs, such as:
            #              'Rewatched': (in diary) review, watched and rewatched 
            #              'Watched':   (in diary) review and watched
            #              'Added': (not in diary) review 
            date = parse_review_date(log_type, date)
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