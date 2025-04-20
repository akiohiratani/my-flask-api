import requests
from bs4 import BeautifulSoup
from typing import List
import re

class SpecialClient:
    USER_AGENT = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
    BASE_SPECIAL_URL = "https://race.netkeiba.com/special/index.html?id={}"

    def __init__(self):
        self.session = requests.Session()
        self.headers = {"User-Agent": self.USER_AGENT}

    def get_soup(self, url: str) -> BeautifulSoup:
        with self.session.get(url, headers=self.headers) as response:
            response.encoding = 'EUC-JP'
            return BeautifulSoup(response.text, 'lxml')

    def get_race_id(self, id:str):
        url = self.BASE_SPECIAL_URL.format(id)
        soup = self.get_soup(url)
        divs = soup.find_all("div", class_="Top_RaceMenu_Inner")
        race_id = None

        for div in divs:
            for link in div.find_all("a", href=True):
                match = re.search(r'race_id=(\d{12})', link['href'])
                if match:
                    race_id = match.group(1)
        return race_id
        