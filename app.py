from flask import Flask, request, jsonify
import requests
import os
import logging
from openai import OpenAI

app = Flask(__name__)

# Webhook URL（GAS）
GAS_URL = "https://script.google.com/macros/s/AKfycby-Jcu-6mLrgNGMHoGavjt9osrY5rv3t21XlnMNKn2qCOb9VOe_T_K_ld6p8kvu86WHcw/exec"
CALENDAR_ID = "zgmf.x20a.39@gmail.com"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=["GET"])
def index():
    return "PRIMROSE Webhook API is running."

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    print("\U0001f4e5 受信したデータ:", data)

    try:
        payload = {
            "title": data.get("title", "No Title"),
            "startTime": data.get("startTime"),
            "endTime": data.get("endTime"),
            "calendarId": data.get("calendarId"),
            "description": data.get("description", "")
        }

        print("\U0001f4e4 GASに送信するデータ:", payload)
        response = requests.post(GAS_URL, json=payload)
        print("\U0001f4e8 GASレスポンス:", response.status_code, response.text)

        return jsonify({"status": "ok", "message": response.text})
    except Exception as e:
        print("❌ 送信エラー:", e)
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/chatgpt-event", methods=["POST"])
def chatgpt_event():
    try:
        data = request.json
        prompt = data.get("prompt")
        if not prompt:
            return jsonify({"status": "error", "message": "Prompt is required."}), 400

        client = OpenAI(api_key=OPENAI_API_KEY)
        functions = [
            {
                "name": "register_event",
                "description": "予定をWebhookに登録します",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string"},
                        "startTime": {"type": "string"},
                        "endTime": {"type": "string"},
                        "calendarId": {"type": "string"},
                        "description": {"type": "string"}
                    },
                    "required": ["title", "startTime", "endTime", "calendarId"]
                }
            }
        ]

        response = client.chat.completions.create(
            model="gpt-4-0613",
            messages=[{"role": "user", "content": prompt}],
            functions=functions,
            function_call="auto"
        )

        arguments = response.choices[0].message.function_call.arguments
        payload = eval(arguments)
        payload["calendarId"] = CALENDAR_ID

        post_response = requests.post("https://primrose-webhook.onrender.com/webhook", json=payload)
        return jsonify({"status": "sent", "result": post_response.text})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.errorhandler(Exception)
def handle_exception(e):
    app.logger.error(f"❌ エラー発生: {e}", exc_info=True)
    return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
