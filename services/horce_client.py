from services.base_client import BaseClient
from bs4 import BeautifulSoup
from typing import List
import re
from typing import List
from output.output import Output

class HorseClient(BaseClient):

    # url
    BASE_URL = "https://db.netkeiba.com/horse/{}"

    # コンストラクタ
    def __init__(self):
        super().__init__()

    # 競走馬の情報を取得
    def get_horses(self, ids:List[str]):
        for id in ids:
            horse = self.get_hours(id)
            break
        return
    def get_hours(self, id:str):
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
        ## db_prof_table
        title = self.get_horse_title(soup)

        return

    def get_horse_base_info(self, soup:BeautifulSoup):
        horse_info = soup.find("div", class_="horse_title")

        #名前の取得
        name = horse_info.find("h1").text
        info = horse_info.find("p", class_="txt_01").text
        sex = info.split('\u3000')
        return {
            "name":name,
            "sex":sex[1]
        }
    
    def get_horse_image(self, soup:BeautifulSoup) -> str:
        main_photo = soup.find(id="HorseMainPhoto")
        image = main_photo.get("src") if main_photo else ""
        return image

    def get_horse_blood(self, soup:BeautifulSoup):
        blood_table = soup.find("table", class_="blood_table")
        horse_names =[]
        if blood_table:
            for td in blood_table.find_all("td"):
                a = td.find("a")
                horse_names.append(a.text)
        return {
            "father":horse_names[0],
            "grandfather":horse_names[1]
        }
    
    def get_horse_title(self, soup:BeautifulSoup):
        #Output().outputTableForClass(soup, "db_prof_table")
        horse_info = {}
        prof_table = soup.find("table", class_="db_prof_table")
        for tr in prof_table.find_all('tr'):
            th = tr.find('th')
            td = tr.find('td')
            if th and td:
                key = th.get_text(strip=True)
                if key == '生年月日':
                    horse_info['birthday'] = td.get_text(strip=True)
                elif key == '主な勝鞍':
                    a = td.find('a')
                    if a:
                        horse_info['title'] = a.get_text(strip=True)
                elif key == '近親馬':
                    relatives = '、'.join([a.get_text(strip=True) for a in td.find_all('a')])
                    horse_info['Close relative'] = relatives
                else:
                    horse_info[key] = td.get_text(strip=True)
        return horse_info["title"]