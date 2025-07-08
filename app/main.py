from flask import Flask, request, jsonify
import os
import requests
import json
from dotenv import load_dotenv
from flask_cors import CORS

from .helper import is_out_of_context, send_alert_email
from .prompt import generate_system_prompt

load_dotenv()

app = Flask(__name__)

# Load config
with open("config.json", "r") as f:
    CONFIG = json.load(f)

cors_origins = CONFIG.get("cors_origins", ["*"])  # fallback to all if not defined
CORS(app, resources={r"/*": {"origins": cors_origins}})

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

@app.route("/chat", methods=["POST"])
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
            "temperature": 0.75
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
