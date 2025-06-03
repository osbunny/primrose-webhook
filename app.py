from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# あなたのGAS公開URLをここに貼ってください
GAS_URL = "https://script.google.com/macros/s/AKfycbxSE8z89e5NJFHvUyl3h52hWs4cGdoMCEmvW6kssTQ2_YYclrYR2F4HRkpGD7Sq5yhXvA/exec"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    print("📥 受信したデータ:", data)

    # GASに中継送信
    response = requests.post(GAS_URL, json=data)

    return jsonify({
        "status": "ok",
        "message": response.text
    })

if __name__ == "__main__":
    app.run(debug=True)
