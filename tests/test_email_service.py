import email

import pytest

from src import email_service
from src.email_service import send_email
from src.models import Config, Participant

CREDENTIALS = {"mail": {"server": "smtp.test", "email": "santa@test.com", "password": "x"}}
CONFIG = Config(budget_limit=None, sender_name="Santa", couples_exclusions=[])


@pytest.fixture
def sent_bodies(monkeypatch):
    bodies = []

    class FakeSMTP:
        def __init__(self, *args):
            pass

        def starttls(self):
            pass

        def login(self, *args):
            pass

        def sendmail(self, sender, recipient, raw_message):
            message = email.message_from_string(raw_message)
            for part in message.walk():
                if part.get_content_type() == "text/plain":
                    bodies.append(part.get_payload(decode=True).decode("utf-8"))

        def quit(self):
            pass

    monkeypatch.setattr(email_service.smtplib, "SMTP", FakeSMTP)
    return bodies


class TestSendEmail:
    def test_send_email_mentions_receiver_email_for_homonyms(self, sent_bodies):
        marie1 = Participant("Marie", "m1@test.com")
        marie2 = Participant("Marie", "m2@test.com")
        bob = Participant("Bob", "bob@test.com")

        send_email(bob, marie2, CONFIG, CREDENTIALS, [marie1, marie2, bob])

        assert "Tu vas faire plaisir à : Marie (m2@test.com)" in sent_bodies[0]

    def test_send_email_plain_name_without_homonym(self, sent_bodies):
        marie = Participant("Marie", "m1@test.com")
        bob = Participant("Bob", "bob@test.com")

        send_email(bob, marie, CONFIG, CREDENTIALS, [marie, bob, Participant("Eve", "eve@test.com")])

        assert "Tu vas faire plaisir à : Marie " in sent_bodies[0]
        assert "m1@test.com" not in sent_bodies[0]
