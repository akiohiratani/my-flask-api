from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List
from models.horce_info import HorseInfoDTO
from services.base_client import BaseClient
from bs4 import BeautifulSoup
import re

class HorseClient(BaseClient):
    BASE_URL = "https://db.netkeiba.com/horse/{}"

    def __init__(self):
        super().__init__()

    def get_horses(self, ids: List[str]) -> List[HorseInfoDTO]:
        # マルチスレッドで馬情報を並列取得
        horses = []
        
        # ThreadPoolExecutorで並列処理
        with ThreadPoolExecutor(max_workers=20) as executor:
            # 各馬IDに対してタスクを登録
            future_to_id = {
                executor.submit(self.get_hours, horse_id): horse_id
                for horse_id in ids
            }
            
            # 完了したタスクから処理
            for future in as_completed(future_to_id):
                horse_id = future_to_id[future]
                try:
                    horse = future.result()
                    horses.append(horse)
                except Exception as e:
                    print(f"馬ID {horse_id} の取得に失敗: {str(e)}")
                    continue
        
        return horses

    def get_hours(self, id: str) -> HorseInfoDTO:
        url = self.BASE_URL.format(id)
        soup = self.get_soup(url)
        
        # 馬の基本情報を取得
        ## 例：ヴァルキリーバース 現役　牝3歳
        horse_info = self.get_horse_base_info(soup)

        # 馬の画像URL取得
        image = self.get_horse_image(soup)

        # 馬の血統を取得
        ## 例：父：エピファネイア, 母父：ハーツクライ
        blood = self.get_horse_blood(soup)

        # 馬の主な勝鞍を取得
        title = self.get_horse_title(soup)
        
        return HorseInfoDTO(
            id=id,
            name=horse_info["name"],
            sex=horse_info["sex"],
            image=image,
            father=blood["father"],
            grandfather=blood["grandfather"],
            title=title
        )

    def get_horse_base_info(self, soup: BeautifulSoup):
        horse_info = soup.find("div", class_="horse_title")
        name = horse_info.find("h1").text
        info = horse_info.find("p", class_="txt_01").text
        sex = info.split('\u3000')
        return {"name": name, "sex": sex[1]}

    def get_horse_image(self, soup: BeautifulSoup) -> str:
        main_photo = soup.find(id="HorseMainPhoto")
        return main_photo.get("src") if main_photo else ""

    def get_horse_blood(self, soup: BeautifulSoup):
        blood_table = soup.find("table", class_="blood_table")
        horse_names = [a.text for td in blood_table.find_all("td") if (a := td.find("a"))]
        return {"father": horse_names[0], "grandfather": horse_names[1]}

    def get_horse_title(self, soup: BeautifulSoup):
        horse_info = {}
        prof_table = soup.find("table", class_="db_prof_table")
        for tr in prof_table.find_all('tr'):
            th, td = tr.find('th'), tr.find('td')
            if th and td:
                key = th.get_text(strip=True)
                if key == '主な勝鞍' and (a := td.find('a')):
                    horse_info['title'] = a.get_text(strip=True)
        return horse_info.get("title", "")
