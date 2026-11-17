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
            couples_exclusions=[("alice@test.com", "bob@test.com")]
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
            couples_exclusions=[("alice@test.com", "bob@test.com"), ("charlie@test.com", "diana@test.com")]
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
            couples_exclusions=[("alice@test.com", "bob@test.com"), ("alice@test.com", "charlie@test.com"), ("bob@test.com", "charlie@test.com")]
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


class TestHomonyms:
    def _participants(self):
        return [
            Participant("Marie", "m1@test.com"),
            Participant("Marie", "m2@test.com"),
            Participant("Bob", "bob@test.com"),
        ]

    def test_homonyms_can_draw_each_other(self):
        participants = self._participants()
        config = Config(budget_limit=None, sender_name="Test", couples_exclusions=[])

        pairs = set()
        for _ in range(200):
            for giver, receiver in create_assignments(participants, config):
                assert giver.email != receiver.email
                pairs.add((giver.email, receiver.email))

        assert ("m1@test.com", "m2@test.com") in pairs or ("m2@test.com", "m1@test.com") in pairs

    def test_couple_exclusion_by_email_does_not_block_homonym(self):
        participants = self._participants() + [Participant("Diana", "diana@test.com")]
        config = Config(
            budget_limit=None,
            sender_name="Test",
            couples_exclusions=[("m1@test.com", "bob@test.com")]
        )

        pairs = set()
        for _ in range(200):
            for giver, receiver in create_assignments(participants, config):
                pairs.add((giver.email, receiver.email))

        assert ("m1@test.com", "bob@test.com") not in pairs
        assert ("bob@test.com", "m1@test.com") not in pairs
        assert ("m2@test.com", "bob@test.com") in pairs
