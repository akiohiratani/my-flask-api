from flask import Blueprint, jsonify, request
from services.horse_name_search_client import HorseNameSearchClient
from services.horce_client import HorseClient

horse_bp = Blueprint('horse', __name__)

@horse_bp.route('/api/v2/horses', methods=['GET'])
def get_horses_info():
    # http://127.0.0.1:5000/api/v2/horses?word=%E3%83%8A%E3%83%9F%E3%83%A5
    search_word = request.args.get('word', '')
    if not search_word:
        return jsonify({"error": {"status_code": 400, "message": "検索語句を指定してください"}}), 400
    try:
        horse_ids = HorseNameSearchClient().search_horse_ids(search_word)
        horses = HorseClient().get_horses(horse_ids)
        return jsonify({"data": [h.to_dict() for h in horses]})
    except Exception as e:
        return jsonify({"error": {"status_code": 500, "message": str(e)}}), 500