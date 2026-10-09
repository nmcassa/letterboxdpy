from letterboxdpy.constants.project import DOMAIN
from letterboxdpy.core.scraper import parse_url
from letterboxdpy.utils.utils_url import get_page_url


class MovieReviews:
    """Movie reviews page operations - user reviews for this movie."""

    def __init__(self, slug: str):
        """Initialize MovieReviews with a movie slug."""
        self.slug = slug
        self.url = f"{DOMAIN}/film/{slug}/reviews"

    def get_all_recent_reviews(self) -> dict:
        """Get all recent reviews (256 pages limit)"""
        return extract_movie_reviews(self.url)
                                     
    def get_all_popular_reviews(self) -> dict:
        """Get all popular reviews (256 pages limit)"""
        url = self.url + "/by/activity"
        return extract_movie_reviews(url)

    def get_reviews_by_rating(self, rating: float) -> dict:
        """Get reviews filtered by rating."""
        return extract_movie_reviews_by_rating(self.url, rating)


def extract_movie_reviews(url: str) -> dict:
    LOGS_PER_PAGE = 12

    page = 0
    data = {"reviews": {}}
    while True:
        page += 1
        dom = parse_url(get_page_url(url, page))

        logs = dom.find_all("article", {"class": ["production-viewing"]})

        if not logs:
            break

        for log in logs:
            review_body = log.find("div", {"class": ["js-review-body"]})

            if not review_body:
                continue

            full_text_url = review_body.get("data-full-text-url")
            if not full_text_url or "viewing:" not in full_text_url:
                continue

            log_id = full_text_url.rstrip("/").split("viewing:")[-1]
            # str ^^^--- log_id: unique id of the review/viewing.

            user = log.find("a", {"class": ["avatar"]})
            user_link = DOMAIN + user["href"] if user and user.get("href") else None
            username = user["href"].strip("/") if user and user.get("href") else None
            # str ^^^--- username: username of the review author.
            # str ^^^--- user_link: link to the review author's profile.

            display_name = log.find("strong", {"class": ["displayname"]})
            display_name = display_name.text.strip() if display_name else None
            # str ^^^--- display_name: display name of the review author.

            rating = log.find("span", {"class": ["inline-rating"]})
            if rating:
                title = rating.find("title")
                rating = title.text.count("★") + title.text.count("½") * 0.5 if title else None
            # float ^^^--- rating: the numerical value of the rating given in the review (0.5-5.0)

            review = "\n\n".join(
                p.get_text(" ", strip=True) for p in review_body.find_all("p")
            ).strip()
            review = review or None
            spoiler = "contains-spoilers" in review_body.get("class", [])
            # str  ^^^--- review: the text content of the review.
            # bool ^^^--- spoiler: whether the review is marked as a spoiler.

            date = log.find("time", {"class": ["timestamp"]})
            date = date["datetime"] if date and date.get("datetime") else None
            # str ^^^--- date: the date of the review.
            #             example: '2026-06-24'

            data["reviews"][log_id] = {
                "user": {
                    "username": username,
                    "display_name": display_name,
                    "link": user_link,
                },
                "rating": rating,
                "review": {"content": review, "spoiler": spoiler},
                "date": date,
            }
            
        if len(logs) < LOGS_PER_PAGE:
            data["count"] = len(data["reviews"])
            data["last_page"] = page
            break

    return data


def extract_movie_reviews_by_rating(url: str, rating: float) -> dict:
    """Extract reviews filtered by specific rating."""

    # TODO: Implement movie reviews by rating extraction
    # This would parse /film/slug/reviews/by/rating/X/ page

    return {"available": False, "rating": rating, "count": 0, "reviews": []}
