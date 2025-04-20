from flask import Blueprint, jsonify, request
from services.schedule_client import ScheduleClient

races_bp = Blueprint('races', __name__)
scheduleClient = ScheduleClient()

@races_bp.route('/api/v2/races', methods=['GET'])
def get_races():
    # ここにロジックを実装
    # 一旦ダミーデータを返す
    # http://127.0.0.1:5000/api/v2/races
    return jsonify({"event": "ダミーレース", "date": "2025-04-20"})

@races_bp.route('/api/v2/races/g_race', methods=['GET'])
def get_topic_race():
    # ここにロジックを実装
    # 一旦ダミーデータを返す
    # http://127.0.0.1:5000/api/v2/races/g_race
    scheduleClient.search_g_race_list()
    return jsonify({"date": "Topick test"})
