from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import json
import os
import sys

from .routes import routes

REQUIRED_ENV_VARS = ["GROQ_API_KEY", "MONITOR_EMAIL", "MONITOR_EMAIL_PASSWORD", "ALERT_RECEIVER_EMAIL"]
REQUIRED_CONFIG_FIELDS = ["bot_name", "user_name", "tech_stack"]

load_dotenv()

def create_app():
    # --- 1. Check for config.json ---
    if not os.path.exists("config.json"):
        print("❌ config.json not found. Please run the setup wizard:\n")
        print("   👉 python setup.py")
        sys.exit(1)

    with open("config.json", "r") as f:
        config = json.load(f)

    missing_fields = [key for key in REQUIRED_CONFIG_FIELDS if key not in config]
    if missing_fields:
        print(f"❌ config.json is missing required fields: {', '.join(missing_fields)}")
        print("   👉 Please re-run: python setup.py")
        sys.exit(1)

    # --- 2. Check for .env variables ---
    missing_env = [var for var in REQUIRED_ENV_VARS if not os.getenv(var)]
    if missing_env:
        print(f"❌ .env is missing required keys: {', '.join(missing_env)}")
        print("   👉 Please re-run: python setup.py")
        sys.exit(1)

    # --- 3. Create and return app ---
    app = Flask(__name__)
    app.config["CONFIG"] = config
    cors_origins = config.get("cors_origins", ["*"])
    CORS(app, resources={r"/*": {"origins": cors_origins}})
    app.register_blueprint(routes)

    return app
