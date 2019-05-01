from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re
import os
import requests

def write_html_file (file_name, file_content):
  file = open(file_name, "w")
  file.write(file_content)
  file.close()

def file_get_contents(filename):
  with open(filename) as f:
    return f.read()

def to_html (request_content):
  return BeautifulSoup(request_content, 'html.parser')

def cache_request (requested_url):
  url_hostname = urlparse(requested_url).hostname
  url_cached_file = 'html_cache/' + url_hostname + '.html'

  if os.path.isfile(url_cached_file):
    file_content = file_get_contents(url_cached_file)
    return to_html(file_content)
  else:
    request = requests.get(requested_url)
    html = to_html(request.content)
    write_html_file(url_cached_file, html.prettify())
    return html