from letterboxdpy.constants.project import DOMAIN
from letterboxdpy.core.scraper import parse_url
from letterboxdpy.pages.user_films import extract_user_films
from letterboxdpy.utils.utils_parser import parse_review_date


class UserLikes:
    """UserLikes class for extracting user's liked content from Letterboxd."""

    def __init__(self, username: str) -> None:
        self.username = username
        self._base_url = f"{DOMAIN}/{self.username}/likes"
        
        # Likes endpoints
        self.films_url = f"{self._base_url}/films"
        self.reviews_url = f"{self._base_url}/reviews/"
        self.lists_url = f"{self._base_url}/lists"

    def get_liked_films(self) -> dict: return extract_user_films(self.films_url)
    def get_liked_reviews(self) -> dict: return extract_liked_reviews(self.reviews_url)
    def get_liked_lists(self) -> dict: return extract_liked_lists(self.lists_url)

def extract_liked_reviews(url: str) -> dict:
    """Extracts liked reviews from the user's likes page."""
    REVIEWS_PER_PAGE = 12
    page = 1
    ret = {'reviews': {}}

    while True:
        dom = parse_url(url + f'/page/{page}')
        items = dom.find_all("article", {"class": ["production-viewing"]})

        for item in items:
            # For production-viewing structure, the review detail is in the body div
            elem_review_detail = item.find("div", {"class": ["body"]})
            if not elem_review_detail:
                continue
                
            # Extract user data
            username = item.get('data-owner', '')
            avatar_link = elem_review_detail.find('a', {"class": "avatar"})
            user_url = DOMAIN + avatar_link['href'] if avatar_link else f"{DOMAIN}/{username}/"
            name_elem = elem_review_detail.find('strong', {'class': 'name'})
            display_name = name_elem.text.strip() if name_elem else username
            review_log_type = "Review"
            
            # Extract movie information from header
            header = elem_review_detail.find("header", {"class": "inline-production-masthead"})
            if not header:
                continue
                
            film_link = header.find("a", href=lambda x: x and "/film/" in x)
            if not film_link:
                continue
                
            movie_name = film_link.text.strip()
            movie_slug = film_link['href'].split('/film/')[-1].rstrip('/')
            movie_url = f"{DOMAIN}/film/{movie_slug}/"
            
            # Look for react-component for movie ID
            react_component = item.find("div", {"class": "react-component"})
            movie_id = react_component.get('data-film-id') if react_component else None
            
            # Look for release year
            movie_release = None
            if header:
                import re
                header_text = header.get_text()
                year_match = re.search(r'\b(19|20)\d{2}\b', header_text)
                if year_match:
                    movie_release = int(year_match.group())

            # Review details
            review_id = item.get('data-object-id', '').split(':')[-1]
            review_url = movie_url  # Default to movie URL
            review_no = 0  # Default value
            
            # Look for rating stars
            review_rating = None
            all_spans = elem_review_detail.find_all("span")
            for span in all_spans:
                classes = span.get('class', [])
                rating_classes = [cls for cls in classes if 'rated-' in str(cls)]
                if rating_classes:
                    try:
                        review_rating = int(rating_classes[0].split('-')[-1])
                        break
                    except (ValueError, IndexError):
                        pass

            # Look for review content
            content_elem = elem_review_detail.find("div", {"class": "body-text"})
            spoiler = False
            review_content = ""
            
            if content_elem:
                spoiler_elem = content_elem.find("p", {"class": lambda x: x and any('spoiler' in str(cls) for cls in x)})
                spoiler = spoiler_elem is not None
                
                paragraphs = content_elem.find_all('p')
                if paragraphs:
                    review_content = '\n'.join([p.get_text().strip() for p in paragraphs if p.get_text().strip()])

            # Look for date
            date_elem = elem_review_detail.find("span", {"class": "_nobr"}) or elem_review_detail.find("time")
            review_date = None
            if date_elem:
                try:
                    review_date = parse_review_date(review_log_type, date_elem)
                except (ValueError, IndexError):
                    review_date = None

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

def extract_liked_lists(url: str) -> dict:
    """Extract liked lists from user's likes page."""
    from letterboxdpy.utils.lists_extractor import ListsExtractor
    
    # Use custom extraction for liked lists (different HTML structure)
    LISTS_PER_PAGE = 12
    page = 1
    data = {'lists': {}}
    
    while True:
        page_url = f"{url}/page/{page}" if page > 1 else url
        dom = parse_url(page_url)
        
        # Find list summaries (liked lists use different HTML structure)
        list_summaries = dom.find_all('article', {'class': 'list-summary'})
        
        for item in list_summaries:
            try:
                list_id = item.get('data-film-list-id')
                if not list_id:
                    continue
                
                # Extract title and URL
                title_elem = item.find('h2', {'class': 'name'})
                if not title_elem or not title_elem.find('a'):
                    continue
                    
                title_link = title_elem.find('a')
                title = title_link.text.strip()
                list_url = DOMAIN + title_link['href']
                slug = title_link['href'].split('/')[-2]
                
                # Extract other data
                value_elem = item.find('span', {'class': 'value'})
                count = int(value_elem.text.strip().split()[0].replace(',', '')) if value_elem else 0
                
                likes_elem = item.find('a', {'class': lambda x: x and 'icon-like' in x})
                likes = 0
                if likes_elem:
                    likes_span = likes_elem.find('span', {'class': 'label'})
                    if likes_span:
                        try:
                            likes = int(likes_span.text.strip())
                        except ValueError:
                            pass
                
                comments_elem = item.find('a', {'class': lambda x: x and 'icon-comment' in x})
                comments = 0
                if comments_elem:
                    comments_span = comments_elem.find('span', {'class': 'label'})
                    if comments_span:
                        try:
                            comments = int(comments_span.text.strip())
                        except ValueError:
                            pass
                
                data['lists'][list_id] = {
                    'title': title,
                    'slug': slug,
                    'description': '',  # Description extraction can be added later
                    'url': list_url,
                    'count': count,
                    'likes': likes,
                    'comments': comments
                }
                
            except Exception:
                continue
        
        if len(list_summaries) < LISTS_PER_PAGE:
            break
        
        page += 1
    
    data['count'] = len(data['lists'])
    data['last_page'] = page
    
    return data