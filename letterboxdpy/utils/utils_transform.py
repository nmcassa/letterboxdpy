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


def get_ajax_url(url: str) -> str:
    """
    Converts a standard discovery URL to the modern CSI discovery API endpoint.
    Letterboxd recently migrated from /films/ajax/ to /csi/films/films-browser-list/.
    """
    # 1. Normalize: Remove legacy '/ajax' path segment if it's already there
    url = url.replace(".com/films/ajax", ".com/films")

    # 2. Redirect discovery traffic to the new CSI internal API
    discovery_base = ".com/films"
    csi_endpoint = ".com/csi/films/films-browser-list"

    # Avoid double-replacement if the URL is already converted
    if csi_endpoint in url:
        return url

    return url.replace(discovery_base, csi_endpoint)
