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
        ## ヴァルキリーバース 現役　牝3歳
        self.get_horse_base_info(soup)

        # 馬の画像URL取得
        image = self.get_horse_image(soup)

        #馬の血統を取得
        ## 父：エピファネイア, 母父：ハーツクライ
        ## db_prof_box
        return
    def get_horse_base_info(self, soup:BeautifulSoup):
        #Output().outputDivForClass(soup, "horse_title")
        horse_info = soup.find("div", class_="horse_title")

        #名前の取得
        name = horse_info.find("h1").text
        info = horse_info.find("p", class_="txt_01").text

        return

    
    def get_horse_image(self, soup:BeautifulSoup) -> str:
        main_photo = soup.find(id="HorseMainPhoto")
        image = main_photo.get("src") if main_photo else ""
        return image