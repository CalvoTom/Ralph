import requests
from bs4 import BeautifulSoup
from api import *
import re

def crawl(url, depth=3):
    visited = set()
    queue = [(url, 0)]

    while queue:
        current_url, current_depth = queue.pop(0)
        if current_url in visited or current_depth > depth:
            continue

        print("Crawling:", current_url)

        try:
            response = requests.get(current_url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                nom_site = soup.title.string.strip()
                titre = soup.title.string.strip()
                corp_de_texte = ' '.join(re.findall(r'\b\w+\b', soup.get_text()))
                add_page(current_url, nom_site, titre, corp_de_texte)

                links = soup.find_all('a', href=True)
                for link in links:
                    new_url = link['href']
                    if new_url.startswith('http'):
                        queue.append((new_url, current_depth + 1))
        except Exception as e:
            print("Error:", e)

        visited.add(current_url)

start_url = "https://google.com"
max_depth = 3
crawl(start_url, max_depth)