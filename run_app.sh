#!/bin/bash

# Script de lancement de l'application Streamlit
echo "🚀 Lancement de l'application Streamlit..."
echo "📊 Analyse du Terrorisme Mondial"
echo ""
echo "L'application va s'ouvrir dans votre navigateur à l'adresse:"
echo "http://localhost:8501"
echo ""
echo "Pour arrêter l'application, utilisez Ctrl+C"
echo ""

# Activation de l'environnement virtuel et lancement de Streamlit
source .venv/bin/activate
streamlit run streamlit_app.py
