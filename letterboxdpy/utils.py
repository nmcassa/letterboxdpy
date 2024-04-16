import re

def extract_numeric_text(tag) -> int:
  try:
    return int(re.sub(r"[^0-9]", '', tag))
  except Exception:
    return None