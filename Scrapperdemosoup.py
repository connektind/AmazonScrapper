import requests
from bs4 import BeautifulSoup

page = requests.get("https://www.amazon.com/s?me=AYBHI2AQPIRDU")
soup = BeautifulSoup(page.content, 'html.parser')
print(soup)