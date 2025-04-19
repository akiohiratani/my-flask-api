from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import urllib.parse
from dataclasses import dataclass, asdict
from typing import List, Optional

# --- 設定値 ---
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)
BASE_LIST_URL = "https://db.netkeiba.com/?pid=horse_list&word={}&match=partial_match"
BASE_DETAIL_URL = "https://db.netkeiba.com{}"
MAX_RESULTS = 3

# --- DTO ---
@dataclass
class HorseDTO:
    id: str
    name: str
    image: str
    sex: str
    birthyear: str
    trainer: str
    sire: str
    mare: str
    bms: str
    owner: str
    breeder: str
    prize: str

    def to_dict(self):
        return asdict(self)

# --- スクレイピング用クライアント ---
class NetkeibaClient:
    def __init__(self):
        self.session = requests.Session()  # セッションを初期化
        self.headers = {"User-Agent": USER_AGENT}

    def get_soup(self, url: str) -> BeautifulSoup:
        with self.session.get(url, headers=self.headers) as response:
            response.encoding = 'EUC-JP'
            return BeautifulSoup(response.text, 'lxml')

    def search_horses(self, word: str) -> List[HorseDTO]:
        print("----------startGetWord----------")
        encoded_word = urllib.parse.quote(word)
        print("----------endGetWord----------")
        print("----------startGetURL----------")
        list_url = BASE_LIST_URL.format(encoded_word)
        print(f"----------EndGetURL-->{list_url}----------")
        print("----------startGetSoup----------")
        soup = self.get_soup(list_url)
        print(f"----------endGetSoup{soup}----------")
        print("----------startGetTable----------")
        table = soup.find("table", class_="nk_tb_common")
        print(f"----------EndGetTable-->{table}----------")
        horses = []
        if table:
            for row in table.find_all("tr")[1:MAX_RESULTS+1]:
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
        detail_url = BASE_DETAIL_URL.format(horse_id)
        soup = self.get_soup(detail_url)

        # 画像パスを取得
        main_photo = soup.find(id="HorseMainPhoto")
        image = main_photo.get("src") if main_photo else ""
        return image

# --- Flaskアプリ ---
app = Flask(__name__)
CORS(app)
client = NetkeibaClient()

@app.errorhandler(400)
def handle_bad_request(error):
    return jsonify({"error": {"status_code": 400, "message": "Bad Request"}}), 400

@app.errorhandler(500)
def handle_internal_error(error):
    return jsonify({"error": {"status_code": 500, "message": "Internal Server Error"}}), 500
@app.route('/', methods=['GET'])
def get_route():
    return "Welcome to Akio Flask API !!!"
@app.route('/api/horses', methods=['GET'])
def get_horses():
    # http://127.0.0.1:5000/api/horses?word=%E3%83%8A%E3%83%9F%E3%83%A5
    search_word = request.args.get('word', '')
    if not search_word:
        return jsonify({"error": {"status_code": 400, "message": "検索語句を指定してください"}}), 400
    try:
        horses = client.search_horses(search_word)
        return jsonify({"data": [h.to_dict() for h in horses]})
    except Exception as e:
        return jsonify({"error": {"status_code": 500, "message": str(e)}}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
