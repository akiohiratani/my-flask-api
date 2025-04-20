import requests
from bs4 import BeautifulSoup
from models.race_info import RaceInfoDTO
from typing import List
from datetime import datetime

class ScheduleClient:
    USER_AGENT = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
    BASE_LIST_URL = "https://race.netkeiba.com/top/schedule.html"

    def __init__(self):
        self.session = requests.Session()
        self.headers = {"User-Agent": self.USER_AGENT}

    def get_soup(self, url: str) -> BeautifulSoup:
        with self.session.get(url, headers=self.headers) as response:
            response.encoding = 'EUC-JP'
            return BeautifulSoup(response.text, 'lxml')

    def search_g_race_list(self):
        todoy_data = datetime.today()
        list_url = self.BASE_LIST_URL.format(todoy_data.year)
        soup = self.get_soup(list_url)
        table = soup.find("table", class_="nk_tb_common race_table_01")
        races = []
        return races
