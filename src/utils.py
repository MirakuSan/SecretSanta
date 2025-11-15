import hashlib
from typing import List, Tuple
from src.models import Participant


def generate_hash(name: str) -> str:
    return hashlib.sha256(name.encode('utf-8')).hexdigest()


def display_hash_verification(assignments: List[Tuple[Participant, Participant]]) -> None:
    print("\n🔐 Vérification manuelle avec SHA256 :")
    print("-" * 80)
    for giver, receiver in assignments:
        giver_hash = generate_hash(giver.name)
        receiver_hash = generate_hash(receiver.name)
        print(f"{giver_hash} offre à {receiver_hash}")
    print("-" * 80)
