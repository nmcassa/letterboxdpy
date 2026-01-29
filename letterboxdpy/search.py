from collections.abc import Callable
from enum import Enum
from itertools import islice
from typing import Any, Iterator

from bs4 import Tag
from fastfingertips.string_utils import extract_number_from_text

from letterboxdpy.avatar import Avatar
from letterboxdpy.constants.project import DOMAIN
from letterboxdpy.core.encoder import Encoder
from letterboxdpy.core.scraper import parse_url, url_encode
from letterboxdpy.utils.utils_file import JsonFile
from letterboxdpy.utils.utils_parser import extract_and_convert_shorthand
from letterboxdpy.utils.utils_string import extract_name_year_from_movie_title


class SearchFilter(Enum):
    ALL = ""
    FILMS = "films"
    REVIEWS = "reviews"
    LISTS = "lists"
    ORIGINAL_LISTS = "original-lists"
    STORIES = "stories"
    CAST_CREW = "cast-crew"
    MEMBERS = "members"
    TAGS = "tags"
    ARTICLES = "articles"
    EPISODES = "episodes"
    FULL_TEXT = "full-text"


class Search:
    SEARCH_URL = f"{DOMAIN}/s/search"
    DEFAULT_NUM_RESULTS = 20
    RESULTS_PER_PAGE = 20
    DEFAULT_NUM_PAGES = DEFAULT_NUM_RESULTS // RESULTS_PER_PAGE

    def __init__(self, query: str, search_filter: SearchFilter | str = SearchFilter.ALL, adult: bool = True,):
        if not isinstance(query, str):
            raise TypeError("query must be a string")

        self.query = url_encode(query)
        self.search_filter = SearchFilter(search_filter)
        self._results = None
        self.url = "/".join(
            filter(None, [self.SEARCH_URL, self.search_filter.value, self.query])
        )
        self.adult = adult

    @property
    def results(self):
        if not self._results:
            self._results = self.get_results()
        return self._results

    def __str__(self):
        return JsonFile.stringify(self.__dict__, indent=2, encoder=Encoder)

    def with_filter(self, search_filter: SearchFilter) -> "Search":
        return Search(self.query, search_filter, adult=self.adult)

    def get_pages(self, num_pages: int = DEFAULT_NUM_PAGES) -> dict[str, Any]:
        return self.get_results(num_pages * self.RESULTS_PER_PAGE)

    def get_results(self, num_results: int = DEFAULT_NUM_RESULTS) -> dict[str, Any]:
        result_item_elems = islice(self.extract_search_results(), num_results)
        result_items = map(self.get_parse_func_from_filter(), result_item_elems)

        results = [{"no": i + 1, "page": (i // self.RESULTS_PER_PAGE) + 1, **result} for i, result in enumerate(result_items)]

        return {
            "available": len(results) > 0,
            "query": self.query,
            "filter": self.search_filter.value,
            "end_page": (len(results) // self.RESULTS_PER_PAGE) + 1,
            "count": len(results),
            "results": results,
        }

    def extract_search_results(self) -> Iterator[Tag]:
        cursor: str | None = None
        while True:
            url = self.get_search_page_url(cursor)
            dom = parse_url(url)
            result_elem = dom.html.body.find("ul", recursive=False)
            if result_elem is None:
                break
            result_item_elems = iter(result_elem.find_all("li", recursive=False))
            while (result_item := next(result_item_elems, None)) is not None:
                yield result_item
            if (cursor := self.get_cursor(result_elem)) is None:
                break

    def get_cursor(self, result_elem: Tag) -> str | None:
        return None if (cursor := result_elem.get("data-cursor")) == "" else cursor

    def get_search_page_url(self, cursor: str | None) -> str:
        params = {"cursor": cursor, "adult": "" if self.adult else None}
        return f"{self.url}/?{'&'.join(f'{k}={v}' for k, v in params.items() if v is not None)}"

    def get_parse_func_from_filter(self) -> Callable[[Tag], dict]:
        match self.search_filter:
            case SearchFilter.FILMS:
                return self.parse_film
            case SearchFilter.REVIEWS:
                return self.parse_review
            case SearchFilter.LISTS | SearchFilter.ORIGINAL_LISTS:
                return self.parse_list
            case SearchFilter.STORIES:
                return self.parse_story
            case SearchFilter.CAST_CREW:
                return self.parse_cast_crew
            case SearchFilter.MEMBERS:
                return self.parse_member
            case SearchFilter.TAGS:
                return self.parse_tag
            case SearchFilter.ARTICLES:
                return self.parse_article
            case SearchFilter.EPISODES:
                return self.parse_episode
            case SearchFilter.ALL | SearchFilter.FULL_TEXT:
                return self.parse_unknown
            case _:
                raise ValueError

    def parse_unknown(self, result_item_elem: Tag) -> dict[str, Any]:
        # Determine the appropriate parsing function by checking the classes on <li> or <article>
        li_class = result_item_elem.get("class")
        match li_class:
            case [_, "-production"]:
                return self.parse_film(result_item_elem)
            case [_, "-viewing"]:
                return self.parse_review(result_item_elem)
            case [_, "-list"]:
                return self.parse_list(result_item_elem)
            case [_, "-contributor", _]:
                return self.parse_cast_crew(result_item_elem)
            case [_, "-person"]:
                return self.parse_member(result_item_elem)
            case [_, "-tag"]:
                return self.parse_tag(result_item_elem)

        article_class = li_class.find("article").get("class")
        match article_class:
            case ["card-summary-journal-article"]:
                return self.parse_article(result_item_elem)
            case ["card-summary", "-graph"]:
                return self.parse_episode(result_item_elem)
            case ["card-summary", "js-card-summary"] | [
                "card-summary",
                "-graph",
                "js-card-summary",
            ]:
                return self.parse_story(result_item_elem)
            case _:
                raise ValueError

    def parse_film(self, result_item_elem: Tag) -> dict[str, Any]:
        film_container = result_item_elem.find("div", class_="react-component figure")
        slug = film_container.get("data-item-slug")
        name = film_container.get("data-item-name")
        title, year = extract_name_year_from_movie_title(name)
        url = f"{DOMAIN}{film_container.get('data-target-link')}"

        def _parse_director(a: Tag) -> dict[str, str]:
            href = a.get("href", "")
            return {
                "name": a.get_text(strip=True),
                "slug": href.split("/")[-2],
                "url": f"{DOMAIN}{href}",
            }

        directors_elem = result_item_elem.find("p", class_="film-metadata")
        directors = None if directors_elem is None else [_parse_director(dir_elem) for dir_elem in directors_elem.find_all("a")]

        return {
            "type": "film",
            "slug": slug,
            "title": title,
            "year": year,
            "url": url,
            "directors": directors,
        }

    def parse_review(self, result_item_elem: Tag) -> dict[str, Any]:
        article = result_item_elem.find("article")
        username = article.get("data-owner")
        user_url = f"{DOMAIN}/{username}"

        movie_container = article.find("div", class_="react-component figure")
        movie_slug = movie_container.get("data-item-slug")
        movie_name = movie_container.get("data-item-name")
        movie_title, movie_year = extract_name_year_from_movie_title(movie_name)
        movie_url = f"{DOMAIN}{movie_container.get('data-item-link')}"

        review_body = article.find("div", class_="body", recursive=False)
        url = review_body.find("h2", class_="name -primary prettify").find("a").get("href")

        display_name_elem = review_body.find("strong", class_="displayname")
        display_name = display_name_elem.get_text()

        rating_elem = review_body.find("span", class_="rating")
        rating = None if rating_elem is None else extract_number_from_text(rating_elem.get("class")[-1]) / 2
        liked_elem = review_body.find("span", class_="label", string="Liked")
        liked = False if liked_elem is None else True

        review_text_elem = review_body.find("div", class_="body-text -prose -reset js-review-body js-collapsible-text")
        full_text = True if review_text_elem.find("div", class_="collapsed-text") is None else False
        review_text =review_text_elem.get_text(strip=True, separator=" ")
        
        review_actions = review_body.find("p", class_="like-link-target react-component")
        likes = extract_number_from_text(review_actions.get("data-count"), join=True)

        return {
            "type": "review",
            "url": url,
            "rating": rating,
            "liked": liked,
            "likes": likes,
            "text": review_text,
            'full_text': full_text,
            "owner": {
                "username": username,
                "display_name": display_name,
                "url": user_url,
            },
            "movie": {
                "title": movie_title,
                "url": movie_url,
                "slug": movie_slug,
                "year": movie_year,
            },
        }

    def parse_list(self, result_item_elem: Tag) -> dict[str, Any]:
        list_body = result_item_elem.find("div", class_="body")
        href_elem = list_body.find("a")
        href = href_elem.get("href")
        url = f"{DOMAIN}{href}"
        username, _, slug = href.split("/")[1:-1]
        owner_url = f"{DOMAIN}/{username}"
        title = href_elem.text
        display_name_elem = href_elem.find_next("strong", class_="displayname")
        display_name = display_name_elem.text

        film_count_elem = list_body.find("span", class_="value")
        film_count = extract_number_from_text(film_count_elem.text)

        like_count_elem = list_body.find("span", class_="label")
        like_count = 0 if like_count_elem is None else extract_and_convert_shorthand(like_count_elem)

        comment_count_elem = list_body.find("span", class_="label")
        comment_count = 0 if comment_count_elem is None else extract_and_convert_shorthand(comment_count_elem)

        text_elem = list_body.find("div", class_="notes body-text -reset -prose")
        text = None if text_elem is None else text_elem.get_text(strip=True)

        return {
            "type": "review",
            "url": url,
            "slug": slug,
            "title": title,
            "films": film_count,
            "likes": like_count,
            "comments": comment_count,
            "text": text,
            "owner": {
                "username": username,
                "display_name": display_name,
                "url": owner_url,
            },
        }

    def parse_story(self, result_item_elem: Tag) -> dict[str, Any]:
        detail_elem = result_item_elem.find("div", class_="detail")
        author_elem = detail_elem.find("a", class_="owner")
        author_href = author_elem.get("href")
        author_url = f"{DOMAIN}{author_href}"
        author_name = author_elem.text

        href_elem = detail_elem.find("h3").find("a")
        href = href_elem.get("href")
        url = f"{DOMAIN}{href}"
        title = href_elem.text

        description_elem = detail_elem.find("div", class_="description body-text -small")
        description = None if description_elem is None else description_elem.text

        return {
            "type": "story",
            "url": url,
            "title": title,
            "description": description,
            "author": {"url": author_url, "name": author_name},
        }

    def parse_cast_crew(self, result_item_elem: Tag) -> dict[str, Any]:
        href_elem = result_item_elem.find("a")
        href = href_elem.get("href")
        name = href_elem.text
        type_, slug = href.split("/")[1:3]
        url = f"{DOMAIN}{href}"

        def _parse_movie(movie_elem: Tag) -> dict[str, str]:
            return {
                "url": f"{DOMAIN}{movie_elem.get('href')}",
                "title": movie_elem.text,
            }

        film_metadata = result_item_elem.find("p", class_="film-metadata")
        movie_list = film_metadata.find_all("a", class_="text-slug")
        popular_movies = list(map(_parse_movie, movie_list))

        return {
            "type": type_,
            "name": name,
            "slug": slug,
            "url": url,
            "popular_movies": popular_movies,
        }

    def parse_member(self, result_item_elem: Tag) -> dict[str, Any]:
        avatar_elem, name_elem = result_item_elem.find_all("a")
        img_elem = avatar_elem.find("img")
        avatar = Avatar(img_elem.get("src")).upscaled_data
        href = name_elem.get("href")
        url = f"{DOMAIN}{href}"
        username = href.split("/")[1]

        name_elem_strings = name_elem.stripped_strings
        display_name = next(name_elem_strings)
        badge = next(name_elem_strings, None)


        return {
            "type": "member",
            "url": url,
            "username": username,
            "display_name": display_name,
            "badge": badge,
            "avatar": avatar,
        }

    def parse_tag(self, result_item_elem: Tag) -> dict[str, str]:
        tag_elem = result_item_elem.find("a")
        return {"tag": tag_elem.get_text(), "url": f"{DOMAIN}{tag_elem.get('href')}"}

    def parse_article(self, result_item_elem: Tag) -> dict[str, Any]:
        detail_elem = result_item_elem.find("div", class_="detail")
        date_elem = detail_elem.find("time")
        date = date_elem.get("datetime")

        href_elem = detail_elem.find("a")
        detail_elem = result_item_elem.find("div", class_="detail")
        href = href_elem.get("href")
        url = f"{DOMAIN}{href}"
        slug = href.split("/")[2]

        title = href_elem.find("h3").get_text()
        teaser = href_elem.find("div", class_="teaser").get_text(strip=True)

        author_elem = detail_elem.find("a", class_="owner")
        author_href = author_elem.get("href")
        author_url = f"{DOMAIN}{author_href}"
        author = author_elem.get_text()

        return {
            "type": "article",
            "url": url,
            "slug": slug,
            "date": date,
            "title": title,
            "teaser": teaser,
            "author": {"name": author, "url": author_url},
        }

    def parse_episode(self, result_item_elem: Tag) -> dict[str, Any]:
        title_elem = result_item_elem.find("h3")
        href_elem = title_elem.find("a")
        href = href_elem.get("href")
        url = f"{DOMAIN}{href}"
        title = href_elem.get_text(strip=True)

        return {"type": "episode", "url": url, "title": title}


# -- FUNCTIONS --

def get_film_slug_from_title(title: str) -> str:
    """
    Helper function to get a film's slug from its title.
    Uses film search to find the best match and returns the slug of the first result.
    
    Args:
        title (str): The film title to search for
        
    Returns:
        str: The film slug if found, None if no results
        
    Example:
        >>> get_film_slug_from_title("The Matrix")
        'the-matrix'
    """
    try:
      query = Search(title, 'films')
      # return first page first result
      return query.get_results(1)['results'][0]['slug']
    except IndexError:
      return None

if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding='utf-8')

    """
    phrase usage:
        q1 = Search("MUBI", 'lists')
        q2 = Search("'MUBI'", 'lists') 
        q1 searches for lists that contain the word 'MUBI' among other possible words
        q2 searches for lists that specifically contain the exact phrase 'MUBI' and
        ... exclude lists that don't contain this phrase

    results usage:
    all page:
        .results
        .get_results()
    filtering:
        .get_results(2)
        .get_results(max=10)

    Note: search pages may sometimes contain previous results. (for now)
    """

    q3 = Search("The") # general search
    q4 = Search("V for Vendetta", 'films')

    # test: instance printing
    print(q3)
    print(q4)

    # test: results
    # print(json.dumps(q3.results, indent=2))
    # print(json.dumps(q4.get_results(), indent=2))
    print(JsonFile.stringify(q3.get_pages(2), indent=2)) # max 2 page result
    print("\n- - -\n"*10)
    print(JsonFile.stringify(q4.get_results(5), indent=2)) #  max 5 result

    # test: slug
    print('slug 1:', get_film_slug_from_title("V for Vendetta"))
    print('slug 2:', get_film_slug_from_title("v for"))
    print('slug 3:', get_film_slug_from_title("VENDETTA"))

    # test: combined
    from letterboxdpy.movie import Movie
    movie_slug = get_film_slug_from_title("V for Vendetta")
    movie_instance = Movie(movie_slug)
    print(movie_instance.description)
