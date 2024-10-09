from datetime import datetime
from letterboxdpy.core.scraper import parse_url
from letterboxdpy.constants.project import DOMAIN


class UserActivity:

    def __init__(self, username: str) -> None:
        self.username = username
        # https://letterboxd.com/<username>/activity/
        self.activity_url = f"{DOMAIN}/ajax/activity-pagination/{self.username}"
        # https://letterboxd.com/<username>/activity/following/
        self.activity_following_url = f"{DOMAIN}/ajax/activity-pagination/{self.username}/following"
        
    def get_activity(self) -> dict: return extract_activity(self.username, self.activity_url)
    def get_activity_following(self) -> dict: return extract_activity(self.username, self.activity_following_url)

def extract_activity(username: str, ajax_url: str) -> dict:

    def get_event_type(section) -> tuple:
        """
        Extracts the event type and log ID from the section.
        """
        event_type = None
        if any(x.startswith('-') for x in section['class']):
            event_type = list(filter(lambda x: x.startswith('-'), section['class']))[0][1:]
        return event_type

    def process_activity_log(section, event_type) -> dict:
        """
        Processes the activity log depending on the event type.
        """
        def parse_datetime(date_string: str) -> datetime:
            """
            Parses a datetime string, handling microseconds if present.
            """
            try:
                return datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S.%fZ')
            except ValueError:
                return datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')

        def process_review_log() -> dict:
            """
            Processes the review-specific log data.
            """
            detail = section.find("div", {"class": "film-detail-content"})
            log_title = detail.p.text.strip()
            log_type = log_title.split()[-1]
            film = detail.h2.find(text=True)

            rating = section.find("span", {"class": ["rating"], })
            rating = int(rating['class'][-1].split('-')[-1]) if rating else None

            film_year = detail.h2.small.text
            film_year = int(film_year) if film_year else None

            review = detail.find("div", {"class": ["body-text"], })
            spoiler = bool(review.find("p", {"class": ["contains-spoilers"], }))
            review = review.find_all('p')[1 if spoiler else 0:]
            review = '\n'.join([p.text for p in review])

            return {
                'type': log_type,
                'title': log_title,
                'film': film,
                'film_year': film_year,
                'rating': rating,
                'spoiler': spoiler,
                'review': review
            }

        def process_basic_log() -> dict:
            """
            Processes the basic log data.
            """
            log_title = section.p.text.strip()
            log_type = log_title.split()[1]
            log_data = {'log_type': log_type, 'title': log_title}

            if log_type == 'followed':
                username = section.find("a", {"class": "target"})['href'].replace('/', '')
                log_data['username'] = username
            elif log_type == 'liked':
                # display_name = section.find("strong",{"class":["name"]}).text.replace('\u2019s',"")
                username = section.find("a", {"class": "target"})['href'].split('/')[1]
                log_data['username'] = username
            elif log_type == 'watched':
                film = section.find("a",{"class":["target"]}).text.split('  ')[-1].strip()
                log_data['film'] = film if film else None

            return log_data

        log_id = section["data-activity-id"]
        date = parse_datetime(section.find("time")['datetime'])
        log_data = {
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
            log_data.update(process_review_log())
        elif event_type == 'basic':
            log_data.update(process_basic_log())

        return {log_id: log_data}

    data = {
        'user': username,
        'logs': {},
        'total_logs': 0
    }

    dom = parse_url(ajax_url)
    sections = dom.find_all("section")

    if not sections:
        # User {username} has no activity.
        return data

    for section in sections:
        event_type = get_event_type(section)
        if event_type in ('review', 'basic'):
            log_data = process_activity_log(section, event_type)
            data['logs'].update(log_data)
            data['total_logs'] = len(data['logs'])
        elif 'no-activity-message' in section['class']:
            break

    return data