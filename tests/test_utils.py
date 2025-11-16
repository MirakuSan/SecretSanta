import pytest
from src.utils import generate_hash, display_hash_verification
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
