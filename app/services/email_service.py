import smtplib
import os
from email.mime.text import MIMEText

from app.core.config import settings


def send_email(to_email: str, subject: str, body: str):

    if os.getenv("LOAD_TEST", "false").lower() == "true":
        print("Skipping email in load test mode")
        return

    msg = MIMEText(body)

    msg["Subject"] = subject
    msg["From"] = settings.SMTP_USER
    msg["To"] = to_email

    try:

        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.set_debuglevel(1)
            server.starttls()
            server.login(
                settings.SMTP_USER,
                settings.SMTP_PASSWORD
            )

            server.send_message(msg)
            print("Email sent successfully")
    except Exception as e:
        print(f"Email sending failed:  {str(e)}")
