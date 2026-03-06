#!/bin/bash
set -e

if ! command -v python3 &> /dev/null; then
    echo "Erreur : Python 3 n'est pas installé. Installe-le depuis https://python.org"
    exit 1
fi

echo "Création de l'environnement virtuel..."
python3 -m venv .venv

echo "Activation de l'environnement..."
source .venv/bin/activate

echo "Installation des dépendances..."
pip install -r requirements.txt

echo ""
echo "Installation terminée. Lance ./run.sh pour démarrer."
