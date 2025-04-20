from services.base_client import BaseClient
from typing import List
import re

class RaceClient(BaseClient):

    # url
    BASE_URL = "https://race.netkeiba.com/race/shutuba.html?race_id={}&rf=race_submenu"

    # コンストラクタ
    def __init__(self):
        super().__init__()

    # 競走馬の情報を取得
    def get_horses(self, id:str):
        url = self.BASE_URL.format(id)
        soup = self.get_soup(url)
        return