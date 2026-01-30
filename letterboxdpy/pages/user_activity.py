from letterboxdpy.core.scraper import parse_url
from letterboxdpy.constants.project import DOMAIN
from letterboxdpy.utils.date_utils import DateUtils
from letterboxdpy.utils.activity_extractor import (
    parse_activity_datetime, build_time_data, ActivityProcessor
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
        # Initialize processor with section
        processor = ActivityProcessor(section)
        
        log_id = section["data-activity-id"]
        date = parse_activity_datetime(section.find("time")['datetime'])
        log_title = processor.get_log_title()
        log_type = processor.get_log_type()
        log_item_slug = processor.get_log_item_slug()

        # Build activity data structure
        log_data = {
            'activity_type': event_type,
            'timestamp': build_time_data(date),
            'content': {}
        }
        
        # Process content by activity type
        if event_type == 'review':
            content_data = processor.process_review(log_type, log_item_slug)
            log_data['content'] = content_data
        elif event_type == 'basic':
            content_data = processor.process_basic(log_title, log_type, log_item_slug)
            log_data['content'] = content_data
        elif event_type == 'newlist':
            content_data = processor.process_newlist(log_title, log_type)
            log_data['content'] = content_data

        return {log_id: log_data}

    from datetime import datetime
    
    data = {
        'metadata': {
            'export_timestamp': DateUtils.format_to_iso(datetime.now()),
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
        # Create a temporary processor just to get event type
        # Or better, make get_event_type a static method or keep it outside?
        # Let's instantiate it, as it's designed to wrap the section.
        temp_processor = ActivityProcessor(section)
        event_type = temp_processor.get_event_type()
        
        if event_type in ('review', 'basic', 'newlist'):
            log_data = _process_log(section, event_type)
            data['activities'].update(log_data)
            data['metadata']['total_activities'] = len(data['activities'])
        elif 'no-activity-message' in section['class']:
            break

    return data
