import pytest
from src.utils import generate_hash, display_hash_verification, display_name, has_homonym
from src.models import Participant


class TestGenerateHash:
    def test_hash_generation(self):
        hash1 = generate_hash("Alice")
        assert len(hash1) == 64
        assert isinstance(hash1, str)

    def test_same_input_same_hash(self):
        hash1 = generate_hash("Alice")
        hash2 = generate_hash("Alice")
        assert hash1 == hash2

    def test_different_input_different_hash(self):
        hash1 = generate_hash("Alice")
        hash2 = generate_hash("Bob")
        assert hash1 != hash2

    def test_hash_is_hexadecimal(self):
        hash_value = generate_hash("Test")
        try:
            int(hash_value, 16)
            is_hex = True
        except ValueError:
            is_hex = False
        assert is_hex is True


class TestDisplayHashVerification:
    def test_display_hash_verification_no_error(self, capsys):
        assignments = [
            (Participant("Alice", "alice@test.com"), Participant("Bob", "bob@test.com")),
            (Participant("Bob", "bob@test.com"), Participant("Charlie", "charlie@test.com")),
        ]

        display_hash_verification(assignments)

        captured = capsys.readouterr()
        assert "Vérification manuelle avec SHA256" in captured.out
        assert "offre à" in captured.out
        assert len(captured.out.split("\n")) > 3


class TestDisplayName:
    def test_display_name_adds_email_for_homonyms(self):
        marie1 = Participant("Marie", "m1@test.com")
        marie2 = Participant("Marie", "m2@test.com")
        participants = [marie1, marie2, Participant("Bob", "bob@test.com")]

        assert has_homonym(marie2, participants) is True
        assert display_name(marie2, participants) == "Marie (m2@test.com)"

    def test_display_name_plain_when_unique(self):
        bob = Participant("Bob", "bob@test.com")
        participants = [Participant("Marie", "m1@test.com"), bob]

        assert has_homonym(bob, participants) is False
        assert display_name(bob, participants) == "Bob"

    def test_homonym_ignores_case_and_spaces(self):
        marie1 = Participant(" marie ", "m1@test.com")
        marie2 = Participant("Marie", "m2@test.com")

        assert has_homonym(marie1, [marie1, marie2]) is True


class TestHashUsesEmail:
    def test_display_hash_uses_email(self, capsys):
        marie1 = Participant("Marie", "m1@test.com")
        marie2 = Participant("Marie", "m2@test.com")

        display_hash_verification([(marie1, marie2), (marie2, marie1)])

        out = capsys.readouterr().out
        assert f"{generate_hash('m1@test.com')} offre à {generate_hash('m2@test.com')}" in out
        assert f"{generate_hash('m2@test.com')} offre à {generate_hash('m1@test.com')}" in out
