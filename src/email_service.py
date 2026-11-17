import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
from typing import Dict, List
from src.models import Participant, Config
from src.utils import display_name


def get_email_template_no_limit(receiver_name: str, sender_name: str) -> str:
    return f"""Salut !

Cette année encore, le Père Noël secret se prépare ! 🎅

Tu vas faire plaisir à : {receiver_name} 🎁

Prépare un petit cadeau qui fera sourire !

Bisous,
{sender_name} 💖
"""


def get_email_template_with_limit(receiver_name: str, sender_name: str, budget: int) -> str:
    return f"""Salut !

Cette année encore, le Père Noël secret se prépare ! 🎅

Tu vas faire plaisir à : {receiver_name} 🎁

Maximum {budget}€ cette année ! 😱

Bisous,
{sender_name} 💖
"""


def send_email(giver: Participant, receiver: Participant, config: Config, credentials: Dict[str, str],
               participants: List[Participant]) -> None:
    smtp_server = credentials['mail']['server']
    sender_email = credentials['mail']['email']
    password = credentials['mail']['password']
    port = 587

    receiver_label = display_name(receiver, participants)
    if config.budget_limit:
        mail_text = get_email_template_with_limit(receiver_label, config.sender_name, config.budget_limit)
    else:
        mail_text = get_email_template_no_limit(receiver_label, config.sender_name)

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = giver.email
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = "🎅 Le Noël Secret"

    msg.attach(MIMEText(mail_text, 'plain', 'utf-8'))

    smtp = smtplib.SMTP(smtp_server, port)
    smtp.starttls()
    smtp.login(sender_email, password)
    smtp.sendmail(sender_email, giver.email, msg.as_string())
    smtp.quit()

    print(f"✅ Email envoyé à {giver.email}")
