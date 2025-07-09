import smtplib
import os
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

CONFIG_FILE = "config.json"

# 🔹 Load keyword config from config.json once
def load_config():
    try:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print("⚠️ config.json not found. Make sure you ran setup.")
        return {}

CONFIG = load_config()

def is_out_of_context(reply: str, expected_keywords=None, forbidden_phrases=None) -> bool:
    """
    Checks if a bot reply is out of character/context.
    - Must contain at least one expected keyword.
    - Must NOT contain any forbidden phrase.
    """
    lower_reply = reply.lower()
    expected_keywords = expected_keywords or CONFIG.get("expected_keywords", [])
    forbidden_phrases = forbidden_phrases or CONFIG.get("forbidden_phrases", [])

    if expected_keywords and forbidden_phrases:
        if not any(kw.lower() in lower_reply for kw in expected_keywords):
            return True

        if any(bad.lower() in lower_reply for bad in forbidden_phrases):
            return True

    return False

def send_alert_email(subject: str, user_input: str, bot_reply: str):
    """
    Sends an alert email if something goes wrong or out of context.
    """
    sender_email = os.getenv("MONITOR_EMAIL")
    receiver_email = os.getenv("ALERT_RECEIVER_EMAIL")
    app_password = os.getenv("MONITOR_EMAIL_PASSWORD")

    if not all([sender_email, receiver_email, app_password]):
        print("⚠️ Email credentials missing in .env. Skipping alert email.")
        return

    body = f"""
    <h3>🚨 AI Reply Out of Context</h3>
    <p><strong>User asked:</strong> {user_input}</p>
    <p><strong>AI replied:</strong> {bot_reply}</p>
    """

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg.attach(MIMEText(body, "html"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, app_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        print("✅ Alert email sent!")
    except Exception as e:
        print("❌ Failed to send alert email:", str(e))
