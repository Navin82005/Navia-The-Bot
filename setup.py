import json
from pathlib import Path

print("\n============================")
print("🛠️  NAVYA AI SETUP WIZARD")
print("============================\n")
print("Let's configure your personal assistant 👩‍💻\n")

# --- CONFIG.JSON SETUP ---
config = {}

# Bot Identity Section
print("==========================")
print("   BOT IDENTITY SETUP")
print("==========================\n")
config["bot_name"] = input("🤖 Bot Name (e.g., Nova, MyBot): ").strip()
config["bot_gender"] = input("👤 Assistant Role/Identity (e.g., girlfriend, boyfriend, best friend): ").strip()
config["user_name"] = input("👤 Your Name: ").strip()
print("🧠 What should the assistant say about you?")
config["bio"] = input("Short Bio: ").strip()

# Education
print("\n==========================")
print("     EDUCATION SETUP")
print("==========================")
print("(Use '\\n' to separate lines)")
config["education"] = input("🎓 Education: ").strip()

# Tech Stack
print("\n==========================")
print("     TECH STACK SETUP")
print("==========================")
print("(e.g., Python, React, MongoDB)")
config["tech_stack"] = input("💻 Tech Stack: ").strip()

# Socials & Interests
print("\n==========================")
print("   SOCIALS & INTERESTS")
print("==========================")
config["socials"] = input("🔗 Social Links (LinkedIn, GitHub, etc.): ").strip()
config["interests"] = input("🎨 Interests or Hobbies: ").strip()

# Tone & Model
print("\n==========================")
print("     PERSONALITY SETUP")
print("==========================")
print("(e.g., friendly, formal, bubbly, sarcastic)")
config["tone"] = input("🗣️ Bot Tone [default: friendly]: ").strip() or "friendly"
config["model"] = input("🤖 Model [default: llama3-8b-8192]: ").strip() or "llama3-8b-8192"

# Context Filters
print("\n==========================")
print("   CONTEXT FILTER SETUP")
print("==========================")
print("(Used to check for out-of-context replies)")
config["expected_keywords"] = [kw.strip() for kw in input("🧠 Expected Keywords (comma-separated): ").split(",")]
config["forbidden_phrases"] = [fp.strip() for fp in input("🚫 Forbidden Phrases (comma-separated): ").split(",")]

# CORS
print("\n==========================")
print("     SERVER CONFIG")
print("==========================")
print("(Frontend URLs allowed to access the assistant)")
config["cors_origins"] = input("🌐 Allowed Origins (comma-separated or *): ").strip().split(",")

# Save config.json
with open("config.json", "w") as f:
    json.dump(config, f, indent=4)
print("\n✅ config.json created!")

# --- .ENV SETUP ---
print("\n==========================")
print("  ENVIRONMENT VARIABLES")
print("==========================")
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

# Final Summary
print("\n==========================")
print("      SETUP COMPLETE")
print("==========================")
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
