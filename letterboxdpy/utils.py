import re

def extractNumericText(tag) -> int:
  try:
    return int(re.sub(r"[^0-9]", '', tag))
  except Exception as e:
    print(f"Error occurred while parsing for numeric text: {e}")
    return tag.text