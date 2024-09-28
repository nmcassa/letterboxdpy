from letterboxdpy.constants.project import DOMAIN
from letterboxdpy.scraper import parse_url
from letterboxdpy.pages.user_films import extract_user_films
from letterboxdpy.utils.utils_parser import parse_review_date


class UserLikes:
    """
    https://letterboxd.com/<username>/likes/films/
    https://letterboxd.com/<username>/likes/reviews/
    https://letterboxd.com/<username>/likes/lists/
    """

    def __init__(self, username: str) -> None:
        self.username = username
        self.url = f"{DOMAIN}/{self.username}/likes"

    def get_liked_films(self) -> dict: return extract_user_films(f"{self.url}/films/")
    def get_liked_reviews(self) -> dict: return extract_liked_reviews(f"{self.url}/reviews/")
    # feat:def get_liked_lists(self) -> dict: return extract_liked_lists(f"{self.url}/lists/")

def extract_liked_reviews(url: str) -> dict:
    """Extracts liked reviews from the user's likes page."""
    REVIEWS_PER_PAGE = 12
    page = 1
    ret = {'reviews': {}}

    while True:
        dom = parse_url(url + f'/page/{page}')
        container = dom.find("ul", {"class": ["film-list"]})
        items = container.find_all("li", {"class": ["film-detail"]}) if container else []

        for item in items:
            elem_review_detail = item.find("div", {"class": ["film-detail-content"]})
            user_url = DOMAIN + elem_review_detail.find('a', {"class": ["avatar"]})['href']
            username = item['data-owner']
            elem_display_name = elem_review_detail.find('strong', {'class': ['name']})
            review_log_type = elem_display_name.previous_sibling.text.strip().split()[0]
            display_name = elem_display_name.text
            
            # Movie details
            movie_name = elem_review_detail.a.text
            movie_slug = elem_review_detail.parent.div['data-film-slug']
            movie_id = elem_review_detail.parent.div['data-film-id']
            movie_release = int(elem_review_detail.small.text) if elem_review_detail.small else None
            movie_url = f"{DOMAIN}/film/{movie_slug}/"

            # Review details
            review_id = item['data-object-id'].split(':')[-1]
            review_url = DOMAIN + elem_review_detail.a['href']
            review_date = elem_review_detail.find("span", {"class": ["_nobr"]})
            review_no = review_url.split(movie_slug)[-1]
            review_no = int(review_no.replace('/', '')) if review_no.count('/') == 2 else 0
            
            review_rating = elem_review_detail.find("span", {"class": ["rating"]})
            review_rating = int(review_rating['class'][-1].split('-')[-1]) if review_rating else None

            review_content = elem_review_detail.find("div", {"class": ["body-text"]})
            spoiler = bool(review_content.find("p", {"class": ["contains-spoilers"]}))
            review_content = review_content.find_all('p')[1 if spoiler else 0:]
            review_content = '\n'.join([p.text for p in review_content])

            review_date = parse_review_date(review_log_type, review_date)

            ret['reviews'][review_id] = {
                'type': review_log_type,
                'no': review_no,
                'url': review_url,
                'rating': review_rating,
                'review': {
                    'content': review_content,
                    'spoiler': spoiler,
                    'date': review_date,
                },
                'user': {
                    'username': username,
                    'display_name': display_name,
                    'url': user_url
                },
                'movie': {
                    'name': movie_name,
                    'slug': movie_slug,
                    'id': movie_id,
                    'release': movie_release,
                    'url': movie_url,
                },
                'page': page,
            }

        if len(items) < REVIEWS_PER_PAGE:
            break

        page += 1

    return ret