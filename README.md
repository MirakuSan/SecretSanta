<h1 align="center">Secret Santa</h1>
<p>
  <img alt="Version" src="https://img.shields.io/badge/version-3-blue.svg?cacheSeconds=2592000" />
  <a href="https://twitter.com/Kractucs" target="_blank">
    <img alt="Twitter: Kractucs" src="https://img.shields.io/twitter/follow/Kractucs.svg?style=social" />
  </a>
</p>


> Interactive CLI tool to organize Secret Santa draws with email notifications, budget limits, and couple exclusions!

## Features

✨ **Interactive CLI** - User-friendly prompts for all configuration

📧 **Email notifications** - Automatic email sending to all participants

💰 **Budget configuration** - Optional spending limits

👫 **Couple exclusions** - Prevent specific pairs from drawing each other

✅ **Email validation** - Built-in validation and duplicate detection

👯 **Duplicate names** - Two people can share a first name: you are warned and can tell them apart

🔐 **SHA256 verification** - Manual verification with cryptographic hashes

🎯 **Smart algorithm** - Constraint-based assignment with retry logic

## Installation

Requires Python 3.10+. Create a virtual environment and install dependencies:
```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

Working in a [Paradev](#paradev-workspace) workspace? This is done for you.

## Usage

### 1. Setup credentials

Create a `credentials.yml` file:
```bash
cp credentials.yml.dist credentials.yml
```

Edit the file with your SMTP credentials:
```yaml
mail:
  server: "smtp.gmail.com"
  email: "your-email@gmail.com"
  password: "your-password"
```

> **Gmail:** use an [app password](https://myaccount.google.com/apppasswords), not your account password. Google rejects regular passwords over SMTP; app passwords require 2-Step Verification to be enabled.

### 2. Run the interactive script

```bash
.venv/bin/python main.py
```

### 3. Follow the prompts

The script will guide you through:
- **Participant count** - Minimum 3 participants
- **Names and emails** - For each participant. If a name is already taken, you are asked whether to tell them apart (e.g. `Marie D.` / `Marie L.`). If you keep both names, the mail adds the receiver's email so the giver knows who it is
- **Budget limit** - Optional spending limit (€)
- **Sender name** - Name to appear in emails
- **Couple exclusions** - Optional pairs to exclude

### 4. Verify and send

- Review SHA256 hashes for manual verification (each hash is computed from the participant's email, so everyone can find their own line)
- Confirm to send emails to all participants

## Example Workflow

```
🎅 Secret Santa Interactive Setup
==================================================

Combien de participants ? (minimum 3) : 4

📝 Entrez les informations pour 4 participants :

--- Participant 1 ---
Nom : Alice
Email : alice@example.com

--- Participant 2 ---
Nom : Bob
Email : bob@example.com

[...]

Voulez-vous définir un budget limite ? (oui/non) : oui
Budget maximum (€) - entrez 0 pour aucune limite : 25

Nom de l'expéditeur pour les emails : Santa Team

Voulez-vous exclure des paires (couples) ? (oui/non) : oui

Participants disponibles :
1. Alice
2. Bob
3. Charlie
4. Diana

Numéro de la première personne (0 pour terminer) : 1
Numéro de la deuxième personne : 2
✅ Paire ajoutée : Alice ↔ Bob

🎲 Création des assignations...

🔐 Vérification manuelle avec SHA256 :
--------------------------------------------------------------------------------
[hash] offre à [hash]
[...]
--------------------------------------------------------------------------------

📧 Voulez-vous envoyer les emails maintenant ? (oui/non) : oui
📤 Envoi des emails...
✅ Email envoyé à alice@example.com
[...]
✅ Tous les emails ont été envoyés !
```

## Development

### Run tests

```bash
.venv/bin/python -m pytest
```

### Run tests with coverage

```bash
.venv/bin/python -m pytest --cov=src --cov-report=term-missing
```

Tests cover:
- Email and budget validation
- Assignment algorithm with constraints (self, couples, duplicate names)
- Interactive participant input (duplicate-name prompt)
- Email content
- SHA256 hashing
- Data models

### Paradev workspace

The repository ships a Paradev config in `.paradev/`:

- **Setup** (`.paradev/setup.sh`, safe to re-run): creates `.venv` (rebuilt if its Python is older than 3.10 or pip is missing), installs `requirements.txt`, and copies `credentials.yml` from the main checkout when the workspace has none. It never overwrites an existing `credentials.yml`.
- **Default terminal**: runs the test suite. `main.py` is never started automatically, as it is interactive and sends real emails.

## Authors

👤 **Thomas**

* Github: [@Kractucs](https://github.com/Kractucs)

👤 **Damien**

* Github: [@MirakuSan](https://github.com/MirakuSan)
