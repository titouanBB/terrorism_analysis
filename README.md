# 🌍 Analyse du Terrorisme Mondial - Application Streamlit

Cette application Streamlit permet d'explorer et d'analyser la Global Terrorism Database de manière interactive.

## 📊 Fonctionnalités

L'application offre plusieurs onglets d'analyse :

### 1. 📊 Tendances temporelles
- Évolution du nombre d'incidents par année
- Heatmap des incidents par mois et année
- Analyse des tendances temporelles

### 2. 🗺️ Répartition géographique
- Top des pays les plus touchés
- Distribution par région
- Carte mondiale des incidents (si coordonnées disponibles)

### 3. ⚔️ Types d'attaques
- Types d'attaques les plus fréquents
- Types d'armes utilisées
- Analyse des méthodes d'attaque

### 4. 🎯 Cibles
- Types de cibles les plus visées
- Taux de succès des attaques
- Analyse des objectifs

### 5. 📋 Données détaillées
- Visualisation tabulaire des données
- Export des données filtrées en CSV
- Exploration détaillée

## 🔍 Filtres interactifs

- **Période** : Sélectionner une plage d'années
- **Régions** : Filtrer par régions géographiques
- **Types d'attaques** : Filtrer par types d'attaques spécifiques

## 🚀 Installation et lancement

### Méthode 1 : Script automatique
```bash
./run_app.sh
```

### Méthode 2 : Manuel
```bash
# Activer l'environnement virtuel
source .venv/bin/activate

# Lancer l'application
streamlit run streamlit_app.py
```

### Méthode 3 : Première installation
```bash
# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
streamlit run streamlit_app.py
```

## 📁 Structure du projet

```
vic/
├── globalterrorismdb_0522dist.xlsx  # Base de données source
├── streamlit_app.py                 # Application Streamlit principale
├── explore_data.py                  # Script d'exploration des données
├── requirements.txt                 # Dépendances Python
├── run_app.sh                      # Script de lancement
└── README.md                       # Ce fichier
```

## 📈 Données

L'application utilise la Global Terrorism Database qui contient :
- **209,706 incidents** terroristes
- **135 colonnes** de données
- **Période** : 1970 à 2020
- **Couverture** : Mondiale

### Principales variables analysées :
- Localisation (pays, région, ville, coordonnées)
- Temporalité (année, mois, jour)
- Types d'attaques et d'armes
- Cibles et dommages
- Groupes responsables
- Victimes (morts et blessés)

## 🛠️ Technologies utilisées

- **Streamlit** : Interface web interactive
- **Pandas** : Manipulation des données
- **Plotly** : Visualisations interactives
- **NumPy** : Calculs numériques

## 📝 Notes

- Pour des performances optimales, certaines visualisations (comme la carte) peuvent être limitées aux 1000 premiers points
- Les données manquantes sont automatiquement gérées
- L'application est optimisée pour une exploration rapide et intuitive des données

## 🌐 Accès

Une fois lancée, l'application est accessible à l'adresse :
**http://localhost:8501**

Pour arrêter l'application, utilisez `Ctrl+C` dans le terminal.
