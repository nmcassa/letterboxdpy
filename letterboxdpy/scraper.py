from bs4 import BeautifulSoup
import requests
import json

class Scraper:

  def __init__(self, domain: str):
    self.headers = {
      "referer": domain,
      "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
      }
    self.builder = "lxml"

  def get_parsed_page(self, url: str) -> BeautifulSoup:

    try:
      response = requests.get(url, headers=self.headers)
    except requests.RequestException as e:
      raise f"Error connecting to {url}: {e}"

    try:  
      dom = BeautifulSoup(response.text, self.builder)
    except Exception as e:
      raise f"Error parsing response from {url}: {e}"

    if response.status_code != 200:
      message = dom.find("section", {"class": "message"})
      message = message.strong.text if message else None
      messages = json.dumps({
          'code': response.status_code,
          'reason': str(response.reason),
          'url': url,
          'message': message
      }, indent=2)
      raise Exception(messages)

    return dom