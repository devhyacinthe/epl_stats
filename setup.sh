#!/bin/bash
# setup.sh - Script d'installation pour le dashboard

echo "🔧 Installation du dashboard Streamlit..."

# Vérifier Python
python --version || { echo "❌ Python non installé"; exit 1; }

# Créer l'environnement virtuel
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate

# Installer les dépendances
pip install --upgrade pip
pip install -r requirements.txt

# Tester l'installation
echo "🧪 Test des imports..."
python -c "
import streamlit as st
import pandas as pd
print('✅ Streamlit:', st.__version__)
print('✅ Pandas:', pd.__version__)
"

echo "🎉 Installation terminée !"
echo "Pour lancer le dashboard localement:"
echo "  streamlit run src/dashboard.py"