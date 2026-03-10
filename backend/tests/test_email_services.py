import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

SMTP_SERVER = os.getenv("MAILJET_SMTP_SERVER")
SMTP_PORT = int(os.getenv("MAILJET_SMTP_PORT"))
USERNAME = os.getenv("MAILJET_USERNAME")
PASSWORD = os.getenv("MAILJET_PASSWORD")
MAIL_FROM = os.getenv("MAIL_FROM")


def send_email(to_email: str, subject: str, body: str):

    msg = MIMEMultipart()
    msg["From"] = MAIL_FROM
    msg["To"] = to_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "html"))

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(USERNAME, PASSWORD)
        server.send_message(msg)