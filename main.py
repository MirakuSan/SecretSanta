#!/usr/bin/env python3

import yaml
from src.user_input import get_participants, get_config
from src.assignment import create_assignments, AssignmentError
from src.email_service import send_email
from src.utils import display_hash_verification


def main():
    print("🎅 Secret Santa Interactive Setup")
    print("=" * 50)

    try:
        credentials = yaml.safe_load(open('./credentials.yml'))
    except FileNotFoundError:
        print("\n❌ Erreur : fichier 'credentials.yml' introuvable.")
        print("Créez-le à partir de 'credentials.yml.dist'.")
        return
    except Exception as e:
        print(f"\n❌ Erreur lors du chargement des credentials : {e}")
        return

    try:
        participants = get_participants()
        config = get_config(participants)

        print("\n🎲 Création des assignations...")
        assignments = create_assignments(participants, config)

        display_hash_verification(assignments)

        confirm = input("\n📧 Voulez-vous envoyer les emails maintenant ? (oui/non) : ").strip().lower()
        if confirm in ['oui', 'o', 'yes', 'y']:
            print("\n📤 Envoi des emails...")
            for giver, receiver in assignments:
                send_email(giver, receiver, config, credentials, participants)
            print("\n✅ Tous les emails ont été envoyés !")
        else:
            print("\n❌ Envoi annulé.")

    except AssignmentError as e:
        print(f"\n❌ Erreur : {e}")
    except KeyboardInterrupt:
        print("\n\n❌ Opération annulée par l'utilisateur.")
    except Exception as e:
        print(f"\n❌ Erreur inattendue : {e}")


if __name__ == "__main__":
    main()
