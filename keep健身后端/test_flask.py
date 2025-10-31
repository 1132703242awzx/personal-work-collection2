"""最小Flask测试 - 排查启动问题"""
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({'status': 'ok', 'message': 'Flask is running!'})

if __name__ == '__main__':
    print("Starting minimal Flask app...")
    print("Visit: http://localhost:5001/")
    try:
        app.run(host='0.0.0.0', port=5001, debug=False, use_reloader=False)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
