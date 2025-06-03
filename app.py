from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# あなたのGAS公開URLをここに貼ってください（例として仮URLを入れています）
GAS_URL = "https://script.google.com/macros/s/AKfycbxSE8z89e5NJFHvUyl3h52hWs4cGdoMCEmvW6kssTQ2_YYclrYR2F4HRkpGD7Sq5yhXvA/exec"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    print("📥 受信したデータ:", data)

    try:
        # GASにPOST送信
        response = requests.post(GAS_URL, json=data)
        return jsonify({
            "status": "ok",
            "message": response.text
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

# ← ここが最も重要なRender用の修正点
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)