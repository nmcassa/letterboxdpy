from letterboxdpy.constants.project import MONTH_ABBREVIATIONS

def month_to_index(month_abbreviation):
    """Convert a month abbreviation to its index."""
    try:
        return MONTH_ABBREVIATIONS.index(month_abbreviation) + 1
    except ValueError:
        return None

def index_to_month(month_index):
    """Convert a month index to its abbreviation."""
    if 1 <= month_index <= 12:
        return MONTH_ABBREVIATIONS[month_index - 1]
    return None