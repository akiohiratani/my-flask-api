from services.base_client import BaseClient
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
        Output().outputTable(soup)
        return