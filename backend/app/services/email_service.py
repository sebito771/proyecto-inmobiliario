import smtplib
import os
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()
SMTP_SERVER = os.getenv("MAILJET_SMTP_SERVER", "in-v3.mailjet.com")
SMTP_PORT = int(os.getenv("MAILJET_SMTP_PORT", 587))
USERNAME = os.getenv("MAILJET_USERNAME")
PASSWORD = os.getenv("MAILJET_PASSWORD")
MAIL_FROM = os.getenv("MAIL_FROM")

logger = logging.getLogger(__name__)


def send_email(to_email: str, subject: str, body: str) -> bool:
    try:
        msg = MIMEMultipart()
        msg["From"] = MAIL_FROM
        msg["To"] = to_email
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "html"))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=10) as server:
            server.starttls()
            server.login(USERNAME, PASSWORD)
            server.send_message(msg)

        return True

    except Exception as e:
        logger.error(f"Error sending email: {e}")
        return False