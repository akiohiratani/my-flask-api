import requests
from bs4 import BeautifulSoup
import urllib.parse
from models.horse import HorseDTO
from typing import List

class NetkeibaClient:
    USER_AGENT = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
    BASE_LIST_URL = "https://db.netkeiba.com/?pid=horse_list&word={}&match=partial_match"
    BASE_DETAIL_URL = "https://db.netkeiba.com{}"
    MAX_RESULTS = 3

    def __init__(self):
        self.session = requests.Session()
        self.headers = {"User-Agent": self.USER_AGENT}

    def get_soup(self, url: str) -> BeautifulSoup:
        with self.session.get(url, headers=self.headers) as response:
            response.encoding = 'EUC-JP'
            return BeautifulSoup(response.text, 'lxml')

    def search_horses(self, word: str) -> List[HorseDTO]:
        encoded_word = urllib.parse.quote(word)
        list_url = self.BASE_LIST_URL.format(encoded_word)
        soup = self.get_soup(list_url)
        table = soup.find("table", class_="nk_tb_common")
        horses = []
        if table:
            for row in table.find_all("tr")[1:self.MAX_RESULTS+1]:
                cells = row.find_all("td")
                if len(cells) < 12:
                    continue
                horse_id = cells[1].find("a").get("href") if cells[1].find("a") else ""
                image = self.get_horse_image(horse_id) if horse_id else ""
                horses.append(HorseDTO(
                    id=horse_id,
                    name=cells[1].get_text(strip=True),
                    image=image,
                    sex=cells[2].get_text(strip=True),
                    birthyear=cells[3].get_text(strip=True),
                    trainer=cells[5].get_text(strip=True),
                    sire=cells[6].get_text(strip=True),
                    mare=cells[7].get_text(strip=True),
                    bms=cells[8].get_text(strip=True),
                    owner=cells[9].get_text(strip=True),
                    breeder=cells[10].get_text(strip=True),
                    prize=cells[11].get_text(strip=True)
                ))
        return horses

    def get_horse_image(self, horse_id: str) -> str:
        detail_url = self.BASE_DETAIL_URL.format(horse_id)
        soup = self.get_soup(detail_url)
        main_photo = soup.find(id="HorseMainPhoto")
        image = main_photo.get("src") if main_photo else ""
        return image
