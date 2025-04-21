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

        # 馬の基本情報を取得
        ## ヴァルキリーバース 現役　牝3歳

        # 馬の画像取得
        ## https://cdn.netkeiba.com/img.db/v1.1/show_photo.php?horse_id=2022104764&no=5671&tn=yes&tmp=no

        #馬の血統を取得
        ## 父：エピファネイア, 母父：ハーツクライ

        Output().outputTableForClass(soup, "db_prof_table ")
        return
