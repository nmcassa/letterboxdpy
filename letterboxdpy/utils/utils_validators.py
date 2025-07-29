import re
import validators

def is_url(url) -> bool:
  """
  this function checks if the URL is valid or not,
  and returns a boolean value as the result.
  """
  return validators.url(url)

def is_null_or_empty(value):
    """Check if the given string is null or empty."""
    if value is None or value == "":
        return True
    return False

def is_whitespace_or_empty(value):
    """Check if the given string is whitespace or empty."""
    if not isinstance(value, str):
        return False
    return not value.strip()

def is_non_negative_integer(value):
    """Check if the given value is a non-negative integer."""
    return isinstance(value, int) and value >= 0

def is_valid_email(value):
    """Check if the given string is a valid email address."""
    if not isinstance(value, str):
        return False
    email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return bool(re.match(email_pattern, value))

def is_positive_float(value):
    """Check if the given value is a positive float."""
    try:
        number = float(value)
        return number > 0
    except (ValueError, TypeError):
        return False

def is_boolean(value):
    """Check if the given value is a boolean."""
    return isinstance(value, bool)