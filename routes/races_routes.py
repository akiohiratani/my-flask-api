from flask import Blueprint, jsonify, request
from services.schedule_client import ScheduleClient
from services.get_holidays_usecase import GetHolidaysUsecase

races_bp = Blueprint('races', __name__)
scheduleClient = ScheduleClient()
getHolidaysUsecase = GetHolidaysUsecase()

@races_bp.route('/api/v2/races', methods=['GET'])
def get_races():
    # ここにロジックを実装
    # 一旦ダミーデータを返す
    # http://127.0.0.1:5000/api/v2/races
    return jsonify({"event": "ダミーレース", "date": "2025-04-20"})

@races_bp.route('/api/v2/races/g_race', methods=['GET'])
def get_topic_race():
    # http://127.0.0.1:5000/api/v2/races/g_race
    try:
        days = getHolidaysUsecase.execute()
        race_list = scheduleClient.search_g_race_list(days)
        return jsonify({"data": [r.to_dict() for r in race_list ]})
    except Exception as e:
        return jsonify({"error": {"status_code": 500, "message": str(e)}}), 500