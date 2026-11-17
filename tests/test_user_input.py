import pytest

from src import user_input
from src.models import Participant
from src.user_input import find_homonym, get_participants


@pytest.fixture
def answers(monkeypatch):
    def feed(*values):
        queue = list(values)
        monkeypatch.setattr("builtins.input", lambda prompt="": queue.pop(0))
        return queue
    return feed


class TestFindHomonym:
    def test_finds_same_name_ignoring_case_and_spaces(self):
        marie = Participant("Marie", "m1@test.com")
        assert find_homonym("  marie ", [marie]) is marie

    def test_returns_none_when_unique(self):
        assert find_homonym("Bob", [Participant("Marie", "m1@test.com")]) is None


class TestHomonymPrompt:
    def test_homonym_prompt_rename_both(self, answers, capsys):
        queue = answers(
            "3",
            "Marie", "m1@test.com",
            "Marie", "oui", "Marie D.", "Marie L.", "m2@test.com",
            "Bob", "bob@test.com",
        )

        participants = get_participants()

        assert [(p.name, p.email) for p in participants] == [
            ("Marie D.", "m1@test.com"),
            ("Marie L.", "m2@test.com"),
            ("Bob", "bob@test.com"),
        ]
        assert "est déjà utilisé" in capsys.readouterr().out
        assert queue == []

    def test_homonym_prompt_keep(self, answers):
        answers(
            "3",
            "Marie", "m1@test.com",
            "Marie", "non", "m2@test.com",
            "Bob", "bob@test.com",
        )

        participants = get_participants()

        assert [p.name for p in participants] == ["Marie", "Marie", "Bob"]

    def test_homonym_prompt_enter_keeps_name(self, answers):
        answers(
            "3",
            "Marie", "m1@test.com",
            "Marie", "oui", "", "", "m2@test.com",
            "Bob", "bob@test.com",
        )

        participants = get_participants()

        assert [p.name for p in participants] == ["Marie", "Marie", "Bob"]

    def test_renamed_to_existing_name_reprompts(self, answers, capsys):
        queue = answers(
            "3",
            "Bob", "bob@test.com",
            "Marie", "m1@test.com",
            "Marie", "oui", "Marie D.", "Bob", "non", "m2@test.com",
        )

        participants = get_participants()

        assert [p.name for p in participants] == ["Bob", "Marie D.", "Bob"]
        assert capsys.readouterr().out.count("est déjà utilisé") == 2
        assert queue == []

    def test_renaming_existing_to_taken_name_reprompts(self, answers, capsys):
        queue = answers(
            "3",
            "Bob", "bob@test.com",
            "Marie", "m1@test.com",
            "Marie", "oui", "Bob", "Marie D.", "Marie L.", "m2@test.com",
        )

        participants = get_participants()

        assert [p.name for p in participants] == ["Bob", "Marie D.", "Marie L."]
        assert "❌ « Bob » est déjà utilisé (bob@test.com)." in capsys.readouterr().out
        assert queue == []
