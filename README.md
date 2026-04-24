# Analyse du Terrorisme Mondial

Une application interactive pour explorer et analyser les données mondiales sur le terrorisme.

## Qu'est-ce que cette application ?

C'est une application web (Streamlit) qui vous permet de :
- **Voir les tendances** : Comment le nombre d'attaques terroristes a changé au fil des années
- **Localiser les attaques** : Quels pays et régions sont les plus affectés
- **Analyser les attaques** : Quels types d'attaques sont les plus courants et quelles armes sont utilisées
- **Comprendre les cibles** : Qui ou quoi est ciblé par ces attaques
- **Filtrer les données** : Analyser les données par période, région ou type d'attaque

## Installation

### Méthode la plus simple (recommandée)

```bash
make all
```

Cela va automatiquement :
1. Créer un environnement virtuel Python
2. Installer toutes les dépendances nécessaires
3. Préparer les données

### Ou manuellement

```bash
# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
streamlit run streamlit_app.py
```

## Utilisation

Après installation, lancez l'application avec :

```bash
make run
```

Ou directement :

```bash
streamlit run streamlit_app.py
```

L'application s'ouvrira dans votre navigateur à l'adresse `http://localhost:8501`

## Les différents onglets

1. **Tendances temporelles** - Graphiques montrant comment les attaques ont évolué avec le temps

2. **Répartition géographique** - Carte et statistiques des pays et régions les plus touchés

3. **Types d'attaques** - Types d'attaques et d'armes les plus utilisées

4. **Cibles** - Analyse de qui ou quoi est visé (gouvernement, civils, militaires, etc.)

5. **Données détaillées** - Tableau avec toutes les informations pour explorer en détail

## Commandes disponibles

```bash
make all        # Installation complète
make setup      # Configuration de l'environnement
make run        # Lancer l'application
make explore    # Analyser les données en console
make clean      # Supprimer l'installation
make help       # Voir toutes les commandes
```

## Fichiers du projet

- `streamlit_app.py` - L'application principale
- `analyze_data.py` - Analyse des données
- `requirements.txt` - Les dépendances Python
- `run_app.sh` - Script de lancement simple
- `Makefile` - Commandes pratiques

## :material/trending_up: Données

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

## :material/build: Technologies utilisées

- **Streamlit** : Interface web interactive
- **Pandas** : Manipulation des données
- **Plotly** : Visualisations interactives
- **NumPy** : Calculs numériques

## :material/edit_note: Notes

- Pour des performances optimales, certaines visualisations (comme la carte) peuvent être limitées aux 1000 premiers points
- Les données manquantes sont automatiquement gérées
- L'application est optimisée pour une exploration rapide et intuitive des données

## :material/public: Accès

Une fois lancée, l'application est accessible à l'adresse :
**http://localhost:8501**

Pour arrêter l'application, utilisez `Ctrl+C` dans le terminal.
