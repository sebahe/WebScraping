import requests
from bs4 import BeautifulSoup
import json

# URL example based on previous scraping
url = 'https://www.veterinariaalem.com/comida-para-perros/agility/'
HEADERS = {'User-Agent': 'Mozilla/5.0'}
response = requests.get(url, headers=HEADERS)
soup = BeautifulSoup(response.content, 'html.parser')
script_tags = soup.find_all('script', type='application/ld+json')

for tag in script_tags:
    data = json.loads(tag.string)
    if isinstance(data, list):
        print(json.dumps(data, indent=2))
        break
    elif isinstance(data, dict):
        print(json.dumps(data, indent=2))
        break
