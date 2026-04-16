import smtplib
from email.mime.text import MIMEText

def send_email(msg_text):
    sender = "your_email@gmail.com"
    password = "your_app_password"

    msg = MIMEText(msg_text)
    msg['Subject'] = "Event Alert"
    msg['From'] = sender
    msg['To'] = sender

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender, password)
        server.send_message(msg)
