from typing import List, Tuple
from random import shuffle
from src.models import Participant, Config


class AssignmentError(Exception):
    pass


def create_assignments(participants: List[Participant], config: Config, max_retries: int = 1000) -> List[Tuple[Participant, Participant]]:
    if len(participants) < 3:
        raise AssignmentError("Il faut au moins 3 participants.")

    attempts = 0

    while attempts < max_retries:
        attempts += 1

        givers = participants[:]
        receivers = participants[:]
        shuffle(receivers)

        assignments = []
        valid = True

        for i, giver in enumerate(givers):
            receiver = receivers[i]

            if giver.name == receiver.name:
                valid = False
                break

            for exclusion in config.couples_exclusions:
                if (giver.name == exclusion[0] and receiver.name == exclusion[1]) or \
                   (giver.name == exclusion[1] and receiver.name == exclusion[0]):
                    valid = False
                    break

            if not valid:
                break

            assignments.append((giver, receiver))

        if valid:
            return assignments

    raise AssignmentError(f"Impossible de créer une assignation valide après {max_retries} tentatives. Vérifiez les contraintes.")
