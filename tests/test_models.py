import pytest
from src.models import Participant, Config


class TestParticipant:
    def test_participant_creation(self):
        p = Participant("Alice", "alice@test.com")
        assert p.name == "Alice"
        assert p.email == "alice@test.com"

    def test_participant_equality(self):
        p1 = Participant("Alice", "alice@test.com")
        p2 = Participant("Alice", "alice@test.com")
        assert p1 == p2

    def test_participant_inequality(self):
        p1 = Participant("Alice", "alice@test.com")
        p2 = Participant("Bob", "bob@test.com")
        assert p1 != p2


class TestConfig:
    def test_config_creation_with_budget(self):
        config = Config(
            budget_limit=25,
            sender_name="Santa",
            couples_exclusions=[("Alice", "Bob")]
        )
        assert config.budget_limit == 25
        assert config.sender_name == "Santa"
        assert config.couples_exclusions == [("Alice", "Bob")]

    def test_config_creation_without_budget(self):
        config = Config(
            budget_limit=None,
            sender_name="Santa",
            couples_exclusions=[]
        )
        assert config.budget_limit is None
        assert config.sender_name == "Santa"
        assert config.couples_exclusions == []

    def test_config_with_multiple_exclusions(self):
        exclusions = [("Alice", "Bob"), ("Charlie", "Diana")]
        config = Config(
            budget_limit=50,
            sender_name="Test",
            couples_exclusions=exclusions
        )
        assert len(config.couples_exclusions) == 2
        assert ("Alice", "Bob") in config.couples_exclusions
        assert ("Charlie", "Diana") in config.couples_exclusions
