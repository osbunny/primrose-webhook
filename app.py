from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

GAS_URL = "https://script.google.com/macros/s/AKfycby-Jcu-6mLrgNGMHoGavjt9osrY5rv3t21XlnMNKn2qCOb9VOe_T_K_ld6p8kvu86WHcw/exec"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    print("📥 受信したデータ:", data)

    try:
        # 必要項目だけ抽出して送信用payloadを明示的に作成
        payload = {
            "title": data.get("title", "No Title"),
            "startTime": data.get("startTime"),
            "endTime": data.get("endTime"),
            "calendarId": data.get("calendarId"),
            "description": data.get("description", "")
        }

        print("📤 GASに送信するデータ:", payload)

        response = requests.post(GAS_URL, json=payload)
        print("📨 GASレスポンス:", response.status_code, response.text)

        return jsonify({
            "status": "ok",
            "message": response.text
        })
    except Exception as e:
        print("❌ 送信エラー:", e)
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)