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

            if giver.email == receiver.email:
                valid = False
                break

            for exclusion in config.couples_exclusions:
                if (giver.email == exclusion[0] and receiver.email == exclusion[1]) or \
                   (giver.email == exclusion[1] and receiver.email == exclusion[0]):
                    valid = False
                    break

            if not valid:
                break

            assignments.append((giver, receiver))

        if valid:
            return assignments

    raise AssignmentError(f"Impossible de créer une assignation valide après {max_retries} tentatives. Vérifiez les contraintes.")
