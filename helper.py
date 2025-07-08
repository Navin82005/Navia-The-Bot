import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os


def is_out_of_context(reply: str, expected_keywords: list[str], forbidden_phrases: list[str]) -> bool:
    """
    Checks if a bot reply is out of character/context.
    - Must contain at least one expected keyword.
    - Must NOT contain any forbidden phrase.
    """
    lower_reply = reply.lower()

    if not any(kw.lower() in lower_reply for kw in expected_keywords):
        return True

    if any(bad.lower() in lower_reply for bad in forbidden_phrases):
        return True

    return False


def send_alert_email(subject: str, user_input: str, bot_reply: str):
    """
    Sends an alert email if something goes wrong or out of context.
    """
    sender_email = os.getenv("MONITOR_EMAIL")           # e.g. navyathebot@gmail.com
    receiver_email = os.getenv("ALERT_RECEIVER_EMAIL")  # your email
    app_password = os.getenv("MONITOR_EMAIL_PASSWORD")  # App Password (NOT your Gmail password)

    if not all([sender_email, receiver_email, app_password]):
        print("⚠️ Environment variables missing for email config.")
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
