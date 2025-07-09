import json
from pathlib import Path
from extractor import start_extraction_process
from dotenv import load_dotenv
import os

print("\n============================")
print("🛠️  NAVYA AI SETUP WIZARD")
print("============================\n")
print("Let's configure your personal assistant 👩‍💻\n")

# --- .ENV SETUP FIRST ---
print("==========================")
print("  ENVIRONMENT VARIABLES")
print("Enter your private credentials (used securely)")

groq_api_key = input("🔑 GROQ API Key: ").strip()
monitor_email = input("📧 Monitor Gmail Address: ").strip()
monitor_password = input("🔑 App Password for Gmail: ").strip()
alert_receiver = input("📥 Alert Receiver Email: ").strip()

env_content = f"""GROQ_API_KEY={groq_api_key}
MONITOR_EMAIL={monitor_email}
MONITOR_EMAIL_PASSWORD={monitor_password}
ALERT_RECEIVER_EMAIL={alert_receiver}
"""

Path(".env").write_text(env_content)
print("✅ .env file created!")

load_dotenv()

# --- CONFIG.JSON SETUP ---
config = {}

# Ask if user wants to use resume
use_resume = input("\n📄 Do you want to generate config from a resume? (y/n): ").strip().lower()
if use_resume in ["", "y", "yes"]:
    start_extraction_process()
    if Path("config.json").exists():
        with open("config.json", "r") as f:
            config = json.load(f)

# Bot Identity Section
print("==========================")
print("   BOT IDENTITY SETUP")

config["bot_name"] = input(f"🤖 Bot Name [Default: {config.get('bot_name', 'Navya')}]: ").strip() or config.get("bot_name", "Navya")
config["bot_gender"] = input(f"👤 Assistant Role/Identity [Default: {config.get('bot_gender', 'Assistant')}]: ").strip() or config.get("bot_gender", "Assistant")
config["user_name"] = input(f"👤 Your Name [Default: {config.get('name', config.get('user_name', ''))}]: ").strip() or config.get("name", config.get("user_name", ""))

# Only ask if not present
if not config.get("bio"):
    print("🧠 What should the assistant say about you?")
    config["bio"] = input("Short Bio: ").strip()

if not config.get("education"):
    print("\n==========================")
    print("     EDUCATION SETUP")
    print("(Use '\\n' to separate lines)")
    config["education"] = input("🎓 Education: ").strip()

if not config.get("tech_stack"):
    print("\n==========================")
    print("     TECH STACK SETUP")
    print("(e.g., Python, React, MongoDB)")
    config["tech_stack"] = input("💻 Tech Stack: ").strip()

if not config.get("socials"):
    print("\n==========================")
    print("   SOCIALS & INTERESTS")
    config["socials"] = input("🔗 Social Links: ").strip()

config["interests"] = input(f"🎨 Interests or Hobbies [Default: {config.get('interests', '')}]: ").strip() or config.get("interests", "")

# Tone & Model
print("\n==========================")
print("     PERSONALITY SETUP")
print("(e.g., friendly, formal, bubbly, sarcastic)")
config["tone"] = input(f"🗣️ Bot Tone [Default: {config.get('tone', 'friendly')}]: ").strip() or config.get("tone", "friendly")
config["model"] = input(f"🤖 Model [Default: {config.get('model', 'llama3-8b-8192')}]: ").strip() or config.get("model", "llama3-8b-8192")

# Context Filters
print("\n==========================")
print("   CONTEXT FILTER SETUP")
print("(Used to check for out-of-context replies)")

kw_input = input(f"🧠 Expected Keywords [Default: {', '.join(config.get('expected_keywords', []))}]: ")
config["expected_keywords"] = [kw.strip() for kw in kw_input.split(",")] if kw_input else config.get("expected_keywords", [])

fp_input = input(f"🚫 Forbidden Phrases [Default: {', '.join(config.get('forbidden_phrases', []))}]: ")
config["forbidden_phrases"] = [fp.strip() for fp in fp_input.split(",")] if fp_input else config.get("forbidden_phrases", [])

# CORS
print("\n==========================")
print("     SERVER CONFIG")
print("(Frontend URLs allowed to access the assistant)")
config["cors_origins"] = input(f"🌐 Allowed Origins [Default: {', '.join(config.get('cors_origins', ['*']))}]: ").strip().split(",") or config.get("cors_origins", ["*"])

# Save config.json
with open("config.json", "w") as f:
    json.dump(config, f, indent=4)
print("\n✅ config.json created!")

# Final Summary
print("\n==========================")
print("      SETUP COMPLETE")
print(f"""
🚀 Your Assistant: {config['bot_name']} ({config['bot_gender']})
🧠 Trained to know everything about: {config['user_name']}

📂 Project Structure:
├── run.py               → Start the assistant
├── config.json          → Stores your assistant's knowledge & tone
├── .env                 → API keys and email credentials (DO NOT SHARE)
├── app/
│   ├── main.py          → Flask backend server
│   ├── helper.py        → Context and alert logic
│   └── prompt.py        → Dynamic prompt generation (if used)

📌 Available Commands:
▶️  Run the assistant:
    python run.py

🛠️  Rerun the setup wizard (anytime):
    py setup.py

🔒 Don't forget:
- Keep your `.env` file safe and secret
- Use `config.json` to customize the assistant's style and memory

💖 Thank you for using Navya AI — your smart, personalized assistant!
""")
