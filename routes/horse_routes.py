from flask import Blueprint, jsonify, request
from services.netkeiba_client import NetkeibaClient

horse_bp = Blueprint('horse', __name__)
client = NetkeibaClient()

@horse_bp.route('/api/horses', methods=['GET'])
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
