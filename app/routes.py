from flask import Blueprint, request, jsonify
import os
import requests
from dotenv import load_dotenv

from .helper import is_out_of_context, send_alert_email, CONFIG
from .prompt import generate_system_prompt

load_dotenv()

routes = Blueprint("routes", __name__)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

@routes.route("/chat", methods=["POST"])
def chat_with_ai():
    try:
        data = request.get_json()
        user_message = data.get("message", "")
        if not user_message:
            return jsonify({"error": "Message field is required"}), 400

        payload = {
            "model": CONFIG.get("model", "llama3-8b-8192"),
            "messages": [
                {"role": "system", "content": generate_system_prompt(CONFIG)},
                {"role": "user", "content": user_message}
            ],
            "temperature": int(0.75 if not CONFIG.get("creativeness") else CONFIG.get("creativeness"))
        }

        response = requests.post(GROQ_API_URL, headers=HEADERS, json=payload)
        response_data = response.json()
        reply = response_data["choices"][0]["message"]["content"]

        if is_out_of_context(reply, CONFIG["expected_keywords"], CONFIG["forbidden_phrases"]):
            send_alert_email(
                subject="🚨 Out-of-context Reply Detected",
                user_input=user_message,
                bot_reply=reply
            )

        return jsonify({"response": reply}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
