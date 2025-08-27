from letterboxdpy.core.scraper import parse_url
from letterboxdpy.constants.project import DOMAIN
from letterboxdpy.utils.activity_extractor import (
    parse_activity_datetime, build_time_data, get_event_type, get_log_title, 
    get_log_type, process_review_activity, process_basic_activity, 
    process_newlist_activity, get_log_item_slug
)


class UserActivity:

    def __init__(self, username: str) -> None:
        self.username = username
        self._base_url = f"{DOMAIN}/ajax/activity-pagination/{self.username}"
        
        # Activity endpoints
        self.activity_url = self._base_url
        self.activity_following_url = f"{self._base_url}/following"
        
    def get_activity(self) -> dict: return extract_activity(self.activity_url)
    def get_activity_following(self) -> dict: return extract_activity(self.activity_following_url)

def extract_activity(ajax_url: str) -> dict:

   def _process_log(section, event_type) -> dict:
       """Process activity log depending on event type."""
       log_id = section["data-activity-id"]
       date = parse_activity_datetime(section.find("time")['datetime'])
       log_title = get_log_title(section)
       log_type = get_log_type(event_type, section)
       log_item_slug = get_log_item_slug(event_type, section)

       log_data = {
           'event_type': event_type,
           'log_type': log_type,
           'title': log_title,
           'time': build_time_data(date),
           'item_slug': log_item_slug
       }

       if event_type == 'review':
           review_data = process_review_activity(section, log_type)
           if review_data.get('film'):
               log_data['film'] = review_data['film']
           if review_data.get('film_year'):
               log_data['film_year'] = review_data['film_year']
           if review_data.get('rating'):
               log_data['rating'] = review_data['rating']
           if review_data.get('review'):
               log_data['review'] = review_data['review']
           if review_data.get('spoiler'):
               log_data['spoiler'] = review_data['spoiler']
       elif event_type == 'basic':
           basic_data = process_basic_activity(section, log_title, log_type)
           if basic_data.get('username'):
               log_data['username'] = basic_data['username']
           if basic_data.get('film'):
               log_data['film'] = basic_data['film']
           if basic_data.get('comment'):
               log_data['comment'] = basic_data['comment']
           if basic_data.get('target_url'):
               log_data['target_url'] = basic_data['target_url']
           if basic_data.get('cloned_list'):
               log_data['cloned_list'] = basic_data['cloned_list']
       elif event_type == 'newlist':
           newlist_data = process_newlist_activity(section, log_title, log_type)
           if newlist_data.get('film_count'):
               log_data['film_count'] = newlist_data['film_count']
           if newlist_data.get('description'):
               log_data['description'] = newlist_data['description']
           if newlist_data.get('likes'):
               log_data['likes'] = newlist_data['likes']
           if newlist_data.get('comments'):
               log_data['comments'] = newlist_data['comments']
           if newlist_data.get('target_list'):
               log_data['target_list'] = newlist_data['target_list']
           if newlist_data.get('source_list'):
               log_data['source_list'] = newlist_data['source_list']

       return {log_id: log_data}

   data = {
       'logs': {},
       'total_logs': 0
   }

   dom = parse_url(ajax_url)
   sections = dom.find_all("section")

   if not sections:
       return data

   for section in sections:
       event_type = get_event_type(section)
       if event_type in ('review', 'basic', 'newlist'):
           log_data = _process_log(section, event_type)
           data['logs'].update(log_data)
           data['total_logs'] = len(data['logs'])
       elif 'no-activity-message' in section['class']:
           break

   return data