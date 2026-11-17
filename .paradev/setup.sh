#!/bin/bash
# Prépare un workspace Paradev : venv Python, dépendances, credentials.
# Idempotent : peut être relancé sans risque (Paradev le relance à chaque boot en cloud).
set -euo pipefail

workspace_root="$(cd "$(dirname "$0")/.." && pwd -P)"
cd "$workspace_root"

# Checkout principal : fourni par Paradev en local, sinon déduit de git.
main_root="${SUPERSET_ROOT_PATH:-$(dirname "$(git rev-parse --path-format=absolute --git-common-dir)")}"

python_is_supported() {
    "$1" -c 'import sys; sys.exit(sys.version_info < (3, 10))' 2>/dev/null
}

if ! command -v python3 >/dev/null 2>&1; then
    echo "❌ python3 introuvable dans le PATH." >&2
    exit 1
fi

if ! python_is_supported python3; then
    echo "❌ Python >= 3.10 requis, trouvé $(python3 --version 2>&1) ($(command -v python3))." >&2
    exit 1
fi

# Un venv créé par un Python trop ancien ou sans pip ne se répare pas tout seul : on le recrée.
if [ -d .venv ] && ! { python_is_supported .venv/bin/python && .venv/bin/python -m pip --version >/dev/null 2>&1; }; then
    echo "♻️  .venv inutilisable (Python trop ancien ou pip absent), recréation"
    rm -rf .venv
fi

if [ ! -d .venv ]; then
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
