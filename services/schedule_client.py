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
    BASE_RACE_URL = "https://race.netkeiba.com/special/"

    def __init__(self):
        self.session = requests.Session()
        self.headers = {"User-Agent": self.USER_AGENT}

    def get_soup(self, url: str) -> BeautifulSoup:
        with self.session.get(url, headers=self.headers) as response:
            response.encoding = 'EUC-JP'
            return BeautifulSoup(response.text, 'lxml')

    def search_g_race_list(self, days: List[str]):
        soup = self.get_soup(self.BASE_LIST_URL)
        table = soup.find("table", class_="nk_tb_common race_table_01")
        races = []
        if(table):
            for row in soup.select('tr.schedule_list3, tr.schedule_list4'):
                cells = row.find_all('td')
                if not cells:
                    continue
                    
                date = cells[0].get_text(strip=True)
                if date not in days:
                    # 指定した日付以外はスキップ
                    continue
                
                # 必要な要素を指定して取得
                race_name_tag = cells[1].find('a')
                race_name = race_name_tag.get_text(strip=True) if race_name_tag else cells[1].get_text(strip=True)
                race_id = race_name_tag['href'].split('id=')[-1] if race_name_tag else ''
                
                races.append({
                    'date': date,
                    'place': cells[3].get_text(strip=True),
                    'race_name': race_name,
                    'url': f"{self.BASE_RACE_URL}{race_id}" if race_id else '',
                    'distance': cells[4].get_text(strip=True)
                })
        return races