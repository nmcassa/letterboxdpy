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
       """Process activity log and extract data."""
       log_id = section["data-activity-id"]
       date = parse_activity_datetime(section.find("time")['datetime'])
       log_title = get_log_title(section)
       log_type = get_log_type(event_type, section)
       log_item_slug = get_log_item_slug(event_type, section)

       # Build activity data structure
       log_data = {
           'activity_type': event_type,
           'timestamp': build_time_data(date),
           'content': {}
       }

       # Process content by activity type
       if event_type == 'review':
           content_data = process_review_activity(section, log_type, log_item_slug)
           log_data['content'] = content_data
       elif event_type == 'basic':
           content_data = process_basic_activity(section, log_title, log_type, log_item_slug)
           log_data['content'] = content_data
       elif event_type == 'newlist':
           content_data = process_newlist_activity(section, log_title, log_type)
           log_data['content'] = content_data

       return {log_id: log_data}

   from datetime import datetime
   
   data = {
       'metadata': {
           'export_timestamp': datetime.now().isoformat(),
           'source_url': ajax_url,
           'total_activities': 0
       },
       'activities': {}
   }

   dom = parse_url(ajax_url)
   sections = dom.find_all("section")

   if not sections:
       return data

   for section in sections:
       event_type = get_event_type(section)
       if event_type in ('review', 'basic', 'newlist'):
           log_data = _process_log(section, event_type)
           data['activities'].update(log_data)
           data['metadata']['total_activities'] = len(data['activities'])
       elif 'no-activity-message' in section['class']:
           break

   return data