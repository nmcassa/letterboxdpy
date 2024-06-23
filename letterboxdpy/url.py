def get_live_feed_url() -> str:
  # total watches and last reviews
  return "https://letterboxd.com/csi/films-live-feed/"

def get_metadata_url() -> str:
  return "https://letterboxd.com/ajax/letterboxd-metadata/"

# -- FILM --

def get_popular_lists_url(film_slug: str) -> str:
  # top lists
  return f"https://letterboxd.com/csi/film/{film_slug}/popular-lists/"

def get_recent_reviews_url(film_slug: str) -> str:
  # last reviews
  return f"https://letterboxd.com/csi/film/{film_slug}/recent-reviews/"

def get_rating_histogram_url(film_slug: str) -> str:
  # fan count and ratings
  return f"https://letterboxd.com/csi/film/{film_slug}/rating-histogram/"

def get_user_actions_url(film_slug: str) -> str:
  return f"https://letterboxd.com/csi/film/{film_slug}/sidebar-user-actions/"

def get_stats_url(film_slug: str) -> str:
  # watches, lists and likes
  return f"https://letterboxd.com/csi/film/{film_slug}/stats/"

def get_news_url(film_slug: str) -> str:
  # posts: journal, video, etc.
  return f"https://letterboxd.com/csi/film/{film_slug}/news/"

def get_availability_url(film_slug: str) -> str:
  # trailer and services
  return f"https://letterboxd.com/csi/film/{film_slug}/availability/"

"""
# -- USER --

def get_user_homepage_url() -> str:
  return "https://letterboxd.com/ajax/user-homepage/"

def get_friend_reviews_url(film_slug: str) -> str:
  return f"https://letterboxd.com/csi/film/{film_slug}/friend-reviews/"

def get_friend_activity_url(film_slug: str) -> str:
  return f"https://letterboxd.com/csi/film/{film_slug}/friend-activity/"

def get_own_reviews_url(film_slug: str) -> str:
  return f"https://letterboxd.com/csi/film/{film_slug}/own-reviews/"

def get_likes_reviews_url(film_slug: str) -> str:
  return "https://letterboxd.com/csi/film/{film_slug}/liked-reviews/"
"""