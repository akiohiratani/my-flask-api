from flask import Flask
from flask_cors import CORS
from routes.horse_routes import horse_bp

app = Flask(__name__)
CORS(app)

# Blueprintの登録
# エンドポイントの登録
app.register_blueprint(horse_bp)

@app.route('/', methods=['GET'])
def get_route():
    # ルートパスへのアクセス時のレスポンス
    return "Welcome to Akio Flask API !!!"

if __name__ == '__main__':
    app.run(debug=True, port=5000)
