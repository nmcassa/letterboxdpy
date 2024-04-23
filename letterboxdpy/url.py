def fetch_stats_url(slug: str) -> str:
  return f"https://letterboxd.com/csi/film/{slug}/stats/"

def fetch_ratings_histogram_url(slug: str) -> str:
  return f"https://letterboxd.com/csi/film/{slug}/rating-histogram/"