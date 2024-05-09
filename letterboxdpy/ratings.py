import unicodedata
from letterboxdpy.utils import extract_numeric_text

rating_conversion = {
  'half-★': 0.5,
  '★': 1,
  '★1⁄2': 1.5,
  '★★': 2,
  '★★1⁄2': 2.5,
  '★★★': 3,
  '★★★1⁄2': 3.5,
  '★★★★': 4,
  '★★★★1⁄2': 4.5,
  '★★★★★': 5,
}

def get_classic_histogram_rating(hist_dom) -> int:
  # NOTE: the rating algorithm is estimated based
  # on prior handling of films before the algorithm update of June 2023
  # was incorporated

  all_rating_el = hist_dom.find_all('li', 'rating-histogram-bar')
  RATING_COUNT_THRESHOLD = 40
  review_count = 0
  total_rating = 0

  for rating_el in all_rating_el:
    if rating_el.a is not None:
      rating_title = rating_el.a.get('title')
      count_and_rating_only = rating_title.split('ratings')
      count_and_rating = unicodedata.normalize('NFKC', count_and_rating_only[0]).split(' ')
      rating_count = extract_numeric_text(count_and_rating[0])
      review_count += rating_count
      total_rating += rating_conversion[count_and_rating[1]] * rating_count
  
  AVERAGE_RATING = total_rating / review_count if review_count > 0 else 0
  RATING_PROPORTION = (RATING_COUNT_THRESHOLD - review_count) / RATING_COUNT_THRESHOLD if review_count < RATING_COUNT_THRESHOLD else 1
  aggregate_rating = AVERAGE_RATING * (1 - RATING_PROPORTION) if RATING_PROPORTION != 1 else AVERAGE_RATING
  standard_rating = 3.5 * RATING_PROPORTION if RATING_PROPORTION != 1 else 0

  return round(standard_rating + aggregate_rating, 2)