import requests
from bs4 import BeautifulSoup
import json

HEADERS = {'User-Agent': 'Mozilla/5.0'}
url = 'https://www.veterinariaalem.com/comida-para-perros/agility/'
response = requests.get(url, headers=HEADERS)
soup = BeautifulSoup(response.content, 'html.parser')
script_tags = soup.find_all('script', type='application/ld+json')

for tag in script_tags:
    data = json.loads(tag.string)
    if isinstance(data, list):
        print(json.dumps(data[0], indent=2))
        break
    elif isinstance(data, dict):
        print(json.dumps(data, indent=2))
        break
