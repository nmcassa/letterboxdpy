"""Date utilities for consistent ISO 8601 format across letterboxdpy."""

from datetime import datetime
from pykit.datetime_utils import parse_datetime


class InvalidDateFormatError(Exception):
    """Raised when date format is not recognized."""
    pass


class DateUtils:
    """Centralized date utilities for consistent date handling."""
    
    ISO_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
    ISO_FORMAT_NO_MICROSECONDS = "%Y-%m-%dT%H:%M:%SZ"
    
    @staticmethod
    def parse_letterboxd_date(date_input) -> datetime | None:
        """Parse various date formats into datetime object."""
        if date_input is None:
            return None
        if isinstance(date_input, datetime):
            return date_input
        if isinstance(date_input, dict):
            return DateUtils._parse_date_dict(date_input)
        if isinstance(date_input, str):
            return DateUtils._parse_date_string(date_input)
        raise InvalidDateFormatError(f"Unsupported date format: {type(date_input)}")
    
    @staticmethod
    def _parse_date_dict(date_dict: dict) -> datetime:
        """Parse date dictionary format."""
        year = date_dict.get('year')
        month = date_dict.get('month')
        day = date_dict.get('day')
        
        if not all(isinstance(x, int) and x is not None for x in [year, month, day]):
            raise InvalidDateFormatError("Invalid date dictionary")
        if not (1 <= month <= 12) or not (1 <= day <= 31):
            raise InvalidDateFormatError("Invalid date values")
            
        return datetime(year, month, day)
    
    @staticmethod
    def _parse_date_string(date_string: str) -> datetime:
        """Parse ISO date string format."""
        dt = parse_datetime(date_string)
        if dt:
            return dt
        raise InvalidDateFormatError(f"Invalid ISO date string: {date_string}")
    
    @staticmethod
    def format_to_iso(date_obj: datetime | None) -> str | None:
        """Format datetime object to ISO 8601 string."""
        if date_obj is None:
            return None
        if not isinstance(date_obj, datetime):
            raise InvalidDateFormatError(f"Expected datetime object, got {type(date_obj)}")
        return date_obj.strftime(DateUtils.ISO_FORMAT)
    
    @staticmethod
    def dict_to_iso(date_dict: dict) -> str:
        """Convert date dictionary to ISO format string."""
        date_obj = DateUtils._parse_date_dict(date_dict)
        return DateUtils.format_to_iso(date_obj)
    
    @staticmethod
    def iso_to_dict(iso_string: str) -> dict:
        """Convert ISO string to date dictionary."""
        date_obj = DateUtils._parse_date_string(iso_string)
        return {'year': date_obj.year, 'month': date_obj.month, 'day': date_obj.day}
    
    @staticmethod
    def to_iso(date_input) -> str | None:
        """Convert any date format to ISO string."""
        date_obj = DateUtils.parse_letterboxd_date(date_input)
        return DateUtils.format_to_iso(date_obj)


# Backward compatibility functions
def parse_activity_datetime(date_string: str) -> datetime:
    """Parse datetime string (backward compatibility)."""
    return DateUtils._parse_date_string(date_string)


def build_time_data(date_obj: datetime) -> str:
    """Build ISO timestamp string (backward compatibility)."""
    return DateUtils.format_to_iso(date_obj)