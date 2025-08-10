if __loader__.name == '__main__':
    import sys
    sys.path.append(sys.path[0] + '/..')

from json import (
  dumps as json_dumps,
  loads as json_loads,
)

from letterboxdpy.utils.utils_parser import extract_numeric_text, get_meta_content
from letterboxdpy.core.decorators import assert_instance
from letterboxdpy.core.scraper import parse_url
from letterboxdpy.core.encoder import Encoder
from letterboxdpy.constants.project import DOMAIN

class Movie:

    def __init__(self, slug: str) -> None:
        assert isinstance(slug, str), f"Movie slug must be a string, not {type(slug)}"

        self.url = f'{DOMAIN}/film/{slug}'
        self.slug = slug

        dom = parse_url(self.url)

        script = dom.find("script", type="application/ld+json")
        script = json_loads(script.text.split('*/')[1].split('/*')[0]) if script else None

        # one line contents
        self.movie_id(dom)
        self.movie_title(dom)
        self.movie_original_title(dom)
        self.movie_runtime(dom)
        self.movie_rating(dom, script)
        self.movie_year(dom, script)
        self.movie_tmdb_link(dom)
        self.movie_imdb_link(dom)
        self.movie_poster(script)
        self.movie_banner(dom)
        self.movie_tagline(dom)
        # long contents
        self.movie_description(dom)
        self.movie_trailer(dom)
        self.movie_alternative_titles(dom)
        self.movie_details(dom)
        self.movie_genres(dom)
        self.movie_cast(dom)
        self.movie_crew(dom)
        self.movie_popular_reviews(dom)

    def __str__(self) -> str:
        return json_dumps(self, indent=2, cls=Encoder)

    def jsonify(self) -> dict:
        return json_loads(self.__str__())

    # letterboxd.com/film/?
    def movie_banner(self, dom) -> str:
        elem = dom.find("div", {"id": ["backdrop"]})
        exists = elem and "data-backdrop2x" in elem.attrs
        self.banner = elem['data-backdrop2x'].split('?')[0] if exists else None

    # letterboxd.com/film/?
    def movie_trailer(self, dom) -> dict:
        elem = dom.find("p", {"class": ["trailer-link"]})

        if elem:
            elem = elem.a['href'].lstrip('/').split('?')[0]
            trailer_id = elem.split('/')[-1]

        self.trailer = {
            'id': trailer_id,
            'link': f"https://www.youtube.com/watch?v={trailer_id}",
            'embed_url': f"https://{elem}",
        } if elem else None
 
    # letterboxd.com/film/?
    def movie_cast(self, dom) -> list:
        data = dom.find("div", {"id": ["tab-cast"]})
        data = data.find_all("a", {"class": {"tooltip"}}) if data else []

        cast = []
        for person in data:

            name = person.text
            role_name = person['title'] if 'title' in person.attrs else None
            url = person['href']
            slug = url.split('/')[-2]
            
            cast.append({
                'name': name,
                'role_name': role_name,
                'slug': slug,
                'url': DOMAIN + url}
                )

        self.cast = cast

    # letterboxd.com/film/?
    def movie_crew(self, dom) -> list:
        data = dom.find("div", {"id": ["tab-crew"]})
        data = data.find_all("a") if data else []

        crew = {}
        for person in data:
            name = person.text
            url = person['href']
  
            job, slug = filter(None, url.split('/'))
            job = job.replace('-', '_')

            if job not in crew:
                crew[job] = []

            crew[job].append({
                'name': name,
                'slug': slug,
                'url': DOMAIN + url}
                )

        self.crew = crew

    # letterboxd.com/film/?
    def movie_details(self, dom) -> list:
        data = dom.find("div", {"id": ["tab-details"]})
        data = data.find_all("a") if data else []

        details = []
        for item in data:
            url_parts = item['href'].split('/')

            _ =  url_parts[1] == 'films'
            item_type, slug = url_parts[1+_:3+_] 

            details.append({
                'type': item_type,
                'name': item.text.strip(),
                'slug': slug,
                'url': DOMAIN + "/".join(url_parts)
            })

        self.details = details

    # letterboxd.com/film/?
    def movie_alternative_titles(self, dom) -> list:
        data = dom.find(attrs={'class': 'text-indentedlist'})
        text = data.text if data else None
        titles = [i.strip() for i in text.split(', ')] if text else None
        self.alternative_titles = titles

    # letterboxd.com/film/?
    def movie_genres(self, dom) -> list:
        data = dom.find(attrs={"id": ["tab-genres"]})
        data = data.find_all("a") if data else []

        genres = []
        for item in data:
            url_parts = item['href'].split('/')
            
            genres.append({
                'type': url_parts[2],
                'name': item.text,
                'slug': url_parts[3],
                'url': DOMAIN + "/".join(url_parts)
            })

        if genres and self.slug == genres[-1]['type']:
            genres.pop() # for show all button

        self.genres = genres

    # letterboxd.com/film/?
    def movie_rating(self, dom, script: dict=None) -> float:
        elem = dom.find('span', attrs={'class': 'average-rating'})
        rating = elem.text if elem else None
        try:
            rating = rating if rating else (
                script['aggregateRating']['ratingValue'] if script else None
                )
            self.rating = float(rating)
        except KeyError:
            self.rating = None

    # letterboxd.com/film/?
    def movie_year(self, dom, script: dict=None) -> int:
        elem = dom.find('div', {'class': 'releaseyear'})
        year = elem.text if elem else None
        try:
            year = year if year else (
                script['releasedEvent'][0]['startDate'] if script else None
                )
            self.year = int(year)
        except (KeyError, ValueError):
            self.year = None

    # letterboxd.com/film/?
    def movie_poster(self, script) -> str:
        # crop: list=(1500, 1000)
        # .replace('230-0-345', f'{crop[0]}-0-{crop[1]}')
        if script:
            poster = script['image'] if 'image' in script else None
            self.poster = poster.split('?')[0] if poster else None
        else:
            self.poster = None

    # letterboxd.com/film/?
    def movie_tagline(self, dom) -> str:
        elem = dom.find(attrs={'class':'tagline'})
        self.tagline = elem.text if elem else None

    # letterboxd.com/film/?
    def movie_description(self, dom) -> str:
        # elem_section = page.find("div", attrs={'class': 'truncate'}).text
        self.description = get_meta_content(dom, name='description')

    # letterboxd.com/film/?
    def movie_popular_reviews(self, dom) -> list:
        container_section = dom.find("section", {"class": ["film-reviews"]})

        def get_text_or_none(element):
            return element.text.strip() if (element and element.text) else None

        def extract_reviewer_username(article):
            return article.get("data-person")

        def extract_reviewer_display_name(article):
            return get_text_or_none(article.find("strong", {"class": ["displayname"]}))

        def extract_review_link(article):
            context_link = article.find("a", {"class": ["context"]})
            href = context_link.get("href") if context_link else None
            return (DOMAIN + href) if href else None

        def extract_rating(article):
            rating_span = article.find("span", {"class": ["rating"]})
            if not (rating_span and rating_span.text):
                for span in article.find_all("span"):
                    classes = span.get("class") or []
                    if any((cls == "rating") or cls.startswith("rating") for cls in classes):
                        rating_span = span
                        break
            return get_text_or_none(rating_span)

        def extract_review_text(article):
            body_div = article.find("div", {"class": ["body-text"]})
            paragraph = body_div.find("p") if body_div else None
            return get_text_or_none(paragraph)

        reviews: list[dict] = []
        if container_section:
            article_elements = container_section.find_all("article", {"class": ["production-viewing"]})
            for article in article_elements:
                reviews.append({
                    "user": {
                        "username": extract_reviewer_username(article),
                        "display_name": extract_reviewer_display_name(article)
                    },  
                    "link": extract_review_link(article),
                    "rating": extract_rating(article),
                    "review": extract_review_text(article),
                })

        self.popular_reviews = reviews

    def movie_id(self, dom) -> str:
        elem = dom.find('span', 'block-flag-wrapper')
        elem = elem.find('a')
        elem = extract_numeric_text(elem.get('data-report-url'))
        self.letterboxd_id = elem

    # letterboxd.com/film/?
    def movie_title(self, dom) -> str:
        h1_elem = dom.find("h1", {"class": ["primaryname"]})
        if h1_elem:
            span_elem = h1_elem.find("span", {"class": ["name"]})
            elem = span_elem.text if span_elem else h1_elem.text
        else:
            elem = dom.find("h1", {"class": ["filmtitle"]})
            elem = elem.text if elem else None
        self.title = elem

    # letterboxd.com/film/?
    def movie_original_title(self, dom) -> str:
        elem = dom.find("h2", {"class": ["originalname"]})
        elem = elem.text.strip() if elem else None
        self.original_title = elem

    # letterboxd.com/film/?
    def movie_runtime(self, dom) -> int:
        elem = dom.find("p", {"class": ["text-footer"]})
        elem = elem.text if elem else None
        #future: extract_numeric_text(elem.split('min')[0])        
        self.runtime = int(
            elem.split('min')[0].replace(',', '').strip()
            ) if elem and 'min' in elem else None

    # letterboxd.com/film/?
    def movie_tmdb_link(self, dom) -> str:
        a = dom.find("a", {"data-track-action": ["TMDB"]})
        self.tmdb_link = a['href'] if a else None

    # letterboxd.com/film/?
    def movie_imdb_link(self, dom) -> str:
        a = dom.find("a", {"data-track-action": ["IMDb"]})
        self.imdb_link = a['href'] if a else None

# -- FUNCTIONS --

# letterboxd.com/film/?/details
@assert_instance(Movie)
def movie_details(movie: Movie) -> dict:
    dom = parse_url("/".join([movie.url, "details"]))
    dom = dom.find("div", {"id": ["tab-details"]})

    data = {
        'country': [],
        'studio': [],
        'language': []
    }

    for a in dom.find_all("a"):
        text = a.text.strip()
        if a['href'][1:7] == 'studio':
            data['studio'].append(text)
        elif a['href'][7:14] == 'country':
            data['country'].append(text)
        elif a['href'][7:15] == 'language':
            data['language'].append(text)

    return data

# letterboxd.com/film/?/members
def movie_watchers(movie: Movie) -> dict:
    """
    Retrieves movie watchers' statistics from the movie's members page.
    """
    BASE_URL = f"{movie.url}/members"

    def extract_watchers_data(dom) -> dict:
        """
        Extracts watchers data from DOM and returns as a dictionary.
        """
        stats = {}
        content_nav = dom.find("div", {"id": "content-nav"})
        if content_nav:
            for a in content_nav.find_all("a", title=True):
                a_text = a.text.strip().lower()
                a_title = a['title']
                count = extract_numeric_text(a_title)
                stats[a_text] = count
        return stats

    try:
        dom = parse_url(BASE_URL)
        return extract_watchers_data(dom)
    except Exception as e:
        raise RuntimeError("Failed to retrieve movie watchers' statistics") from e

if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding='utf-8')

    movie_instance = Movie("v-for-vendetta") # 132 mins
    # movie_instance_2 = Movie("honk-2013") # 1 min
    # movie_instance_3 = Movie("logistics-2011") # 51420 mins

    print(movie_instance)
    print(json_dumps(movie_details(movie_instance), indent=2))
    print(json_dumps(movie_watchers(movie_instance), indent=2))
