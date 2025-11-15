import pytest
from src.assignment import create_assignments, AssignmentError
from src.models import Participant, Config


class TestCreateAssignments:
    def test_basic_assignment(self):
        participants = [
            Participant("Alice", "alice@test.com"),
            Participant("Bob", "bob@test.com"),
            Participant("Charlie", "charlie@test.com"),
        ]
        config = Config(budget_limit=None, sender_name="Test", couples_exclusions=[])

        assignments = create_assignments(participants, config)

        assert len(assignments) == 3
        assert all(giver != receiver for giver, receiver in assignments)

    def test_no_self_assignment(self):
        participants = [
            Participant("Alice", "alice@test.com"),
            Participant("Bob", "bob@test.com"),
            Participant("Charlie", "charlie@test.com"),
        ]
        config = Config(budget_limit=None, sender_name="Test", couples_exclusions=[])

        assignments = create_assignments(participants, config)

        for giver, receiver in assignments:
            assert giver.name != receiver.name

    def test_couple_exclusions(self):
        participants = [
            Participant("Alice", "alice@test.com"),
            Participant("Bob", "bob@test.com"),
            Participant("Charlie", "charlie@test.com"),
            Participant("Diana", "diana@test.com"),
        ]
        config = Config(
            budget_limit=None,
            sender_name="Test",
            couples_exclusions=[("Alice", "Bob")]
        )

        assignments = create_assignments(participants, config)

        for giver, receiver in assignments:
            if giver.name == "Alice":
                assert receiver.name != "Bob"
            if giver.name == "Bob":
                assert receiver.name != "Alice"

    def test_multiple_couple_exclusions(self):
        participants = [
            Participant("Alice", "alice@test.com"),
            Participant("Bob", "bob@test.com"),
            Participant("Charlie", "charlie@test.com"),
            Participant("Diana", "diana@test.com"),
        ]
        config = Config(
            budget_limit=None,
            sender_name="Test",
            couples_exclusions=[("Alice", "Bob"), ("Charlie", "Diana")]
        )

        assignments = create_assignments(participants, config)

        for giver, receiver in assignments:
            if giver.name == "Alice":
                assert receiver.name != "Bob"
            if giver.name == "Bob":
                assert receiver.name != "Alice"
            if giver.name == "Charlie":
                assert receiver.name != "Diana"
            if giver.name == "Diana":
                assert receiver.name != "Charlie"

    def test_less_than_3_participants_raises_error(self):
        participants = [
            Participant("Alice", "alice@test.com"),
            Participant("Bob", "bob@test.com"),
        ]
        config = Config(budget_limit=None, sender_name="Test", couples_exclusions=[])

        with pytest.raises(AssignmentError, match="au moins 3 participants"):
            create_assignments(participants, config)

    def test_impossible_constraints_raises_error(self):
        participants = [
            Participant("Alice", "alice@test.com"),
            Participant("Bob", "bob@test.com"),
            Participant("Charlie", "charlie@test.com"),
        ]
        config = Config(
            budget_limit=None,
            sender_name="Test",
            couples_exclusions=[("Alice", "Bob"), ("Alice", "Charlie"), ("Bob", "Charlie")]
        )

        with pytest.raises(AssignmentError, match="Impossible de créer une assignation valide"):
            create_assignments(participants, config, max_retries=100)

    def test_all_participants_assigned(self):
        participants = [
            Participant("Alice", "alice@test.com"),
            Participant("Bob", "bob@test.com"),
            Participant("Charlie", "charlie@test.com"),
            Participant("Diana", "diana@test.com"),
        ]
        config = Config(budget_limit=None, sender_name="Test", couples_exclusions=[])

        assignments = create_assignments(participants, config)

        givers = {a[0].name for a in assignments}
        receivers = {a[1].name for a in assignments}

        assert len(givers) == 4
        assert len(receivers) == 4
        assert givers == {p.name for p in participants}
        assert receivers == {p.name for p in participants}
