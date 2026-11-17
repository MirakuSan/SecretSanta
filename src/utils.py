import hashlib
from typing import List, Tuple
from src.models import Participant


def generate_hash(name: str) -> str:
    return hashlib.sha256(name.encode('utf-8')).hexdigest()


def normalize_name(name: str) -> str:
    return name.strip().casefold()


def has_homonym(participant: Participant, participants: List[Participant]) -> bool:
    return any(
        other.email != participant.email and normalize_name(other.name) == normalize_name(participant.name)
        for other in participants
    )


def display_name(participant: Participant, participants: List[Participant]) -> str:
    if has_homonym(participant, participants):
        return f"{participant.name} ({participant.email})"
    return participant.name


def display_hash_verification(assignments: List[Tuple[Participant, Participant]]) -> None:
    print("\n🔐 Vérification manuelle avec SHA256 (empreinte de l'email) :")
    print("-" * 80)
    for giver, receiver in assignments:
        giver_hash = generate_hash(giver.email)
        receiver_hash = generate_hash(receiver.email)
        print(f"{giver_hash} offre à {receiver_hash}")
    print("-" * 80)
