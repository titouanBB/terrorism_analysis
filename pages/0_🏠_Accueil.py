import streamlit as st

# Configuration de la page
st.set_page_config(
    page_title="Accueil - Terrorisme Europe",
    page_icon="🏠",
    layout="wide"
)

st.title("🏠 Analyse du Terrorisme en Europe")
st.markdown("---")

# Description de l'application
st.markdown("""
## 🎯 Bienvenue dans l'Analyse du Terrorisme Européen

Cette application interactive vous permet d'explorer les données de terrorisme en Europe de 1970 à 2020, 
basées sur la Global Terrorism Database (GTD).

### 📊 Fonctionnalités Disponibles

""")

# Colonnes pour les différentes sections
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### 🇪🇺 **Vue d'Ensemble Européenne**
    
    **Page principale** - Analyse comparative de tous les pays européens :
    - 📈 Statistiques globales et tendances
    - 🗺️ Comparaisons entre pays
    - 📊 Types d'attaques et évolution temporelle
    - 🎯 Analyse des cibles et groupes terroristes
    
    ➡️ **Naviguer** : Page principale (streamlit_app.py)
    """)
    
    # Bouton pour aller à la page principale
    if st.button("📊 Accéder à l'Analyse Européenne", type="primary"):
        st.switch_page("streamlit_app.py")

with col2:
    st.markdown("""
    ### 🇫🇷 **Focus France Détaillé**
    
    **Page spécialisée** - Analyse approfondie de la France :
    - 🗺️ **Carte interactive** avec localisation précise
    - 📍 Incidents par ville et région  
    - 📅 Filtres temporels avancés
    - 📋 Tableaux détaillés des incidents
    - 📈 Analyses par décennie
    
    ➡️ **Naviguer** : Pages → 🇫🇷 France
    """)
    
    # Bouton pour aller à la page France
    if st.button("🇫🇷 Accéder à l'Analyse France", type="secondary"):
        st.switch_page("pages/1_🇫🇷_France.py")

st.markdown("---")

# Statistiques rapides
st.markdown("### 🔢 Aperçu des Données")

try:
    import pandas as pd
    from setup_data import setup_data
    setup_data()
    
    # Charger les données rapidement
    df = pd.read_excel('globalterrorismdb_0522dist.xlsx')
    
    european_countries = [
        'France', 'Germany', 'United Kingdom', 'Italy', 'Spain', 'Netherlands', 
        'Belgium', 'Greece', 'Portugal', 'Austria', 'Switzerland', 'Denmark',
        'Sweden', 'Norway', 'Finland', 'Ireland', 'Luxembourg', 'Poland',
        'Czech Republic', 'Hungary', 'Slovakia', 'Slovenia', 'Croatia',
        'Romania', 'Bulgaria', 'Estonia', 'Latvia', 'Lithuania', 'Malta', 'Cyprus'
    ]
    
    europe_df = df[df['country_txt'].isin(european_countries)]
    france_df = df[df['country_txt'].str.contains('France', case=False, na=False)]
    
    # Métriques
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "🇪🇺 Incidents Europe", 
            f"{len(europe_df):,}",
            help="Total des incidents terroristes enregistrés en Europe"
        )
    
    with col2:
        st.metric(
            "🇫🇷 Incidents France", 
            f"{len(france_df):,}",
            help="Total des incidents terroristes en France"
        )
    
    with col3:
        period = f"{europe_df['iyear'].min()}-{europe_df['iyear'].max()}"
        st.metric(
            "📅 Période Couverte", 
            period,
            help="Étendue temporelle des données"
        )
    
    with col4:
        countries_count = europe_df['country_txt'].nunique()
        st.metric(
            "🗺️ Pays Européens", 
            f"{countries_count}",
            help="Nombre de pays européens dans l'analyse"
        )
    
    # Top 5 des pays
    st.markdown("### 📊 Top 5 des Pays les Plus Touchés")
    top_countries = europe_df['country_txt'].value_counts().head()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        import plotly.express as px
        fig = px.bar(
            x=top_countries.values,
            y=top_countries.index,
            orientation='h',
            title="Nombre d'incidents par pays",
            labels={'x': 'Nombre d\'incidents', 'y': 'Pays'},
            color=top_countries.values,
            color_continuous_scale='Reds'
        )
        fig.update_layout(showlegend=False, coloraxis_showscale=False, height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("**Répartition :**")
        for i, (country, count) in enumerate(top_countries.items(), 1):
            percentage = (count / len(europe_df)) * 100
            st.markdown(f"{i}. **{country}**: {count:,} ({percentage:.1f}%)")

except Exception as e:
    st.warning(f"Impossible de charger l'aperçu des données : {e}")
    st.info("Les données seront disponibles une fois l'application lancée.")

st.markdown("---")

# Instructions
st.markdown("""
### 🚀 Comment Utiliser l'Application

1. **📊 Vue Générale** : Commencez par la page principale pour avoir une vue d'ensemble de l'Europe
2. **🇫🇷 Analyse Détaillée** : Utilisez la page France pour une exploration approfondie avec carte
3. **🔍 Filtres** : Utilisez les barres latérales pour affiner vos recherches
4. **📋 Export** : Les graphiques peuvent être téléchargés en cliquant sur l'icône appareil photo

### 📚 Source des Données
Les données proviennent de la **Global Terrorism Database (GTD)**, maintenue par l'Université du Maryland. 
Cette base de données est la collection la plus complète d'incidents terroristes dans le monde.

### ⚠️ Note Importante
Cette application est conçue à des fins d'analyse académique et de recherche. Les données présentées 
sont basées sur des sources ouvertes et peuvent contenir des biais ou des erreurs.
""")

st.markdown("---")
st.markdown("*💡 Astuce : Utilisez la barre latérale gauche pour naviguer entre les différentes pages*")