from typing import List, Tuple, Optional
from src.models import Participant, Config
from src.validation import validate_email, validate_budget


def get_participant_count() -> int:
    while True:
        try:
            count = int(input("\nCombien de participants ? (minimum 3) : "))
            if count >= 3:
                return count
            print("❌ Il faut au moins 3 participants.")
        except ValueError:
            print("❌ Veuillez entrer un nombre valide.")


def get_participants() -> List[Participant]:
    count = get_participant_count()
    participants = []
    emails = []

    print(f"\n📝 Entrez les informations pour {count} participants :")

    for i in range(count):
        print(f"\n--- Participant {i+1} ---")

        name = input("Nom : ").strip()
        while not name:
            print("❌ Le nom ne peut pas être vide.")
            name = input("Nom : ").strip()

        while True:
            email = input("Email : ").strip()
            if not validate_email(email):
                print("❌ Email invalide. Réessayez.")
                continue
            if email in emails:
                print("❌ Cet email est déjà utilisé.")
                continue
            break

        participants.append(Participant(name=name, email=email))
        emails.append(email)

    return participants


def get_budget_config() -> Optional[int]:
    while True:
        response = input("\nVoulez-vous définir un budget limite ? (oui/non) : ").strip().lower()
        if response in ['oui', 'o', 'yes', 'y']:
            while True:
                try:
                    budget = int(input("Budget maximum (€) - entrez 0 pour aucune limite : "))
                    if validate_budget(budget):
                        return budget if budget > 0 else None
                    print("❌ Le budget ne peut pas être négatif.")
                except ValueError:
                    print("❌ Veuillez entrer un nombre valide.")
        elif response in ['non', 'n', 'no']:
            return None
        else:
            print("❌ Répondez par 'oui' ou 'non'.")


def get_sender_name() -> str:
    name = input("\nNom de l'expéditeur pour les emails : ").strip()
    while not name:
        print("❌ Le nom ne peut pas être vide.")
        name = input("Nom de l'expéditeur : ").strip()
    return name


def get_couple_exclusions(participants: List[Participant]) -> List[Tuple[str, str]]:
    exclusions = []

    while True:
        response = input("\nVoulez-vous exclure des paires (couples) ? (oui/non) : ").strip().lower()
        if response in ['non', 'n', 'no']:
            break
        elif response in ['oui', 'o', 'yes', 'y']:
            print("\nParticipants disponibles :")
            for i, p in enumerate(participants):
                print(f"{i+1}. {p.name}")

            while True:
                try:
                    person1_idx = int(input("\nNuméro de la première personne (0 pour terminer) : "))
                    if person1_idx == 0:
                        break
                    person2_idx = int(input("Numéro de la deuxième personne : "))

                    if person1_idx < 1 or person1_idx > len(participants):
                        print("❌ Numéro invalide.")
                        continue
                    if person2_idx < 1 or person2_idx > len(participants):
                        print("❌ Numéro invalide.")
                        continue
                    if person1_idx == person2_idx:
                        print("❌ Une personne ne peut pas être en couple avec elle-même.")
                        continue

                    name1 = participants[person1_idx - 1].name
                    name2 = participants[person2_idx - 1].name

                    pair = (name1, name2)
                    reverse_pair = (name2, name1)

                    if pair in exclusions or reverse_pair in exclusions:
                        print(f"❌ Cette paire existe déjà.")
                        continue

                    exclusions.append(pair)
                    print(f"✅ Paire ajoutée : {name1} ↔ {name2}")
                except ValueError:
                    print("❌ Veuillez entrer un nombre valide.")
            break
        else:
            print("❌ Répondez par 'oui' ou 'non'.")

    return exclusions


def get_config(participants: List[Participant]) -> Config:
    budget = get_budget_config()
    sender = get_sender_name()
    couples = get_couple_exclusions(participants)

    return Config(
        budget_limit=budget,
        sender_name=sender,
        couples_exclusions=couples
    )
