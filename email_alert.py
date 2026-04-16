import smtplib
import os
from email.mime.text import MIMEText

def send_email(msg_text):
    sender = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASS")

    msg = MIMEText(msg_text)
    msg['Subject'] = "⚠️ Event Feedback Alert"
    msg['From'] = sender
    msg['To'] = sender

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender, password)
        server.send_message(msg)
