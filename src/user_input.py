from typing import List, Tuple, Optional
from src.models import Participant, Config
from src.validation import validate_email, validate_budget
from src.utils import display_name, normalize_name


def get_participant_count() -> int:
    while True:
        try:
            count = int(input("\nCombien de participants ? (minimum 3) : "))
            if count >= 3:
                return count
            print("❌ Il faut au moins 3 participants.")
        except ValueError:
            print("❌ Veuillez entrer un nombre valide.")


YES_ANSWERS = ['oui', 'o', 'yes', 'y']
NO_ANSWERS = ['non', 'n', 'no']


def ask_yes_no(question: str) -> bool:
    while True:
        response = input(question).strip().lower()
        if response in YES_ANSWERS:
            return True
        if response in NO_ANSWERS:
            return False
        print("❌ Répondez par 'oui' ou 'non'.")


def find_homonym(name: str, participants: List[Participant]) -> Optional[Participant]:
    return next((p for p in participants if normalize_name(p.name) == normalize_name(name)), None)


def ask_new_name(participant: Participant, participants: List[Participant]) -> str:
    others = [p for p in participants if p is not participant]
    while True:
        new_name = input(f"Nom affiché pour {participant.email} [{participant.name}] : ").strip() or participant.name
        clash = find_homonym(new_name, others)
        if clash is None or normalize_name(new_name) == normalize_name(participant.name):
            return new_name
        print(f"❌ « {new_name} » est déjà utilisé ({clash.email}).")


def resolve_homonym(name: str, participants: List[Participant]) -> str:
    """Avertit si le nom est déjà pris et propose de préciser qui est qui.

    Renomme au besoin le participant déjà inscrit, et renvoie le nom de la nouvelle personne.
    """
    while True:
        existing = find_homonym(name, participants)
        if existing is None:
            return name

        print(f"⚠️  Le nom « {existing.name} » est déjà utilisé ({existing.email}).")
        print(f"   Sans précision, les mails ajouteront l'email pour les distinguer, ex. « {existing.name} ({existing.email}) ».")
        if not ask_yes_no("Préciser qui est qui ? (oui/non) : "):
            return name

        existing.name = ask_new_name(existing, participants)
        name = input(f"Nom affiché pour la nouvelle personne [{name}] : ").strip() or name

        # Les deux noms gardés identiques : choix assumé, le mail ajoutera l'email.
        if normalize_name(name) == normalize_name(existing.name):
            return name


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
        name = resolve_homonym(name, participants)

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
                print(f"{i+1}. {display_name(p, participants)}")

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

                    person1 = participants[person1_idx - 1]
                    person2 = participants[person2_idx - 1]
                    name1 = display_name(person1, participants)
                    name2 = display_name(person2, participants)

                    pair = (person1.email, person2.email)
                    reverse_pair = (person2.email, person1.email)

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
