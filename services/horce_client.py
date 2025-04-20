from services.base_client import BaseClient
from typing import List
import re

class HorseClient(BaseClient):

    # url
    BASE_URL = "https://db.netkeiba.com/horse/{}"

    # コンストラクタ
    def __init__(self):
        super().__init__()

    # 競走馬の情報を取得
    def get_horses(self, id:str):
        url = self.BASE_URL.format(id)
        soup = self.get_soup(url)
        return