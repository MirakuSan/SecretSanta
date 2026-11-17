#!/bin/bash
# Prépare un workspace Paradev : venv Python, dépendances, credentials.
# Idempotent : peut être relancé sans risque (Paradev le relance à chaque boot en cloud).
set -euo pipefail

workspace_root="$(cd "$(dirname "$0")/.." && pwd -P)"
cd "$workspace_root"

# Checkout principal : fourni par Paradev en local, sinon déduit de git.
main_root="${SUPERSET_ROOT_PATH:-$(dirname "$(git rev-parse --path-format=absolute --git-common-dir)")}"

if ! command -v python3 >/dev/null 2>&1; then
    echo "❌ python3 introuvable dans le PATH." >&2
    exit 1
fi

if [ ! -x .venv/bin/python ]; then
    echo "🐍 Création du virtualenv .venv"
    python3 -m venv .venv
fi

echo "📦 Installation des dépendances"
.venv/bin/python -m pip install --quiet --disable-pip-version-check -r requirements.txt

main_credentials="$main_root/credentials.yml"
if [ -f credentials.yml ]; then
    echo "🔑 credentials.yml déjà présent, conservé"
elif [ "$(cd "$main_root" && pwd -P)" != "$workspace_root" ] && [ -f "$main_credentials" ]; then
    cp "$main_credentials" credentials.yml
    echo "🔑 credentials.yml copié depuis $main_root"
else
    echo "⚠️  Pas de credentials.yml : copiez credentials.yml.dist en credentials.yml avant d'envoyer des mails."
fi

echo "✅ Workspace prêt"
