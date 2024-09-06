import re

MONTH_ABBREVIATIONS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", 
                       "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

def extract_numeric_text(text: str) -> int:
    """
    Extracts numeric characters from a string and returns them as an integer.
    Returns None if an error occurs.
    """
    try:
        numeric_value = int(re.sub(r"[^0-9]", '', text))
        return numeric_value
    except Exception:
        return None

def parse_review_date(review_log_type, review_date):
    """
    Parses review date depending on log type.
    returns: {'year': 2024, 'month': 1, 'day': 1}
    """
    if review_log_type == 'Added':
        try:
            # ISO 8601 format: '2024-01-01T05:45:00.268Z'
            date_parts = map(int, review_date.time['datetime'][:10].split('-'))
            parsed_date = dict(zip(['year', 'month', 'day'], date_parts))
        except (KeyError, ValueError) as e:
            raise ValueError(f"Error parsing ISO date format: {e}")
    else:
        try:
            # '01 Jan 2024' format
            date_parts = review_date.text.split()
            parsed_date = {
                'year': int(date_parts[2]),
                'month': MONTH_ABBREVIATIONS.index(date_parts[1]) + 1,
                'day': int(date_parts[0])
            }
            
        except (IndexError, ValueError) as e:
            raise ValueError(f"Error parsing written date format: {e}")
    
    return parsed_date