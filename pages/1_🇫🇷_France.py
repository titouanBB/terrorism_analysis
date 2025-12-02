import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Configuration de la page
st.set_page_config(
    page_title="Terrorisme en France",
    page_icon="🇫🇷",
    layout="wide"
)

# Cache pour charger les données
@st.cache_data
def load_france_data():
    """Charge et filtre les données pour la France"""
    try:
        df = pd.read_excel('globalterrorismdb_0522dist.xlsx')
        
        # Filtrer pour la France
        france_data = df[df['country_txt'].str.contains('France', case=False, na=False)].copy()
        
        # Nettoyer les données
        france_data['date'] = pd.to_datetime(france_data[['iyear', 'imonth', 'iday']], errors='coerce')
        
        # Remplacer les valeurs manquantes dans les colonnes importantes
        france_data['city'] = france_data['city'].fillna('Lieu non spécifié')
        france_data['provstate'] = france_data['provstate'].fillna('Région non spécifiée')
        france_data['attacktype1_txt'] = france_data['attacktype1_txt'].fillna('Type non spécifié')
        france_data['targtype1_txt'] = france_data['targtype1_txt'].fillna('Cible non spécifiée')
        france_data['gname'] = france_data['gname'].fillna('Groupe inconnu')
        france_data['weaptype1_txt'] = france_data['weaptype1_txt'].fillna('Arme non spécifiée')
        france_data['nkill'] = france_data['nkill'].fillna(0)
        france_data['nwound'] = france_data['nwound'].fillna(0)
        
        return france_data, df
        
    except Exception as e:
        st.error(f"Erreur lors du chargement des données: {e}")
        return None, None

# Titre principal
st.title("🇫🇷 Analyse du Terrorisme en France")
st.markdown("---")

# Charger les données
france_data, _ = load_france_data()

if france_data is not None and len(france_data) > 0:
    
    # Métriques principales
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("🎯 Total Incidents", f"{len(france_data):,}")
    
    with col2:
        total_kills = int(france_data['nkill'].sum())
        st.metric("💀 Total Victimes", f"{total_kills:,}")
    
    with col3:
        total_wounded = int(france_data['nwound'].sum())
        st.metric("🏥 Total Blessés", f"{total_wounded:,}")
    
    with col4:
        periode = f"{france_data['iyear'].min()}-{france_data['iyear'].max()}"
        st.metric("📅 Période", periode)
    
    with col5:
        cities_count = france_data['city'].nunique()
        st.metric("🏙️ Villes Touchées", f"{cities_count:,}")

    st.markdown("---")

    # Sidebar pour les filtres
    with st.sidebar:
        st.header("🔍 Filtres")
        
        # Filtre par années
        years = sorted(france_data['iyear'].unique())
        year_range = st.select_slider(
            "Période",
            options=years,
            value=(years[0], years[-1])
        )
        
        # Filtre par région
        regions = ['Toutes'] + sorted(france_data['provstate'].unique().tolist())
        selected_region = st.selectbox("Région", regions)
        
        # Filtre par type d'attaque
        attack_types = ['Tous'] + sorted(france_data['attacktype1_txt'].unique().tolist())
        selected_attack = st.selectbox("Type d'attaque", attack_types)

    # Appliquer les filtres
    filtered_data = france_data[
        (france_data['iyear'] >= year_range[0]) & 
        (france_data['iyear'] <= year_range[1])
    ]
    
    if selected_region != 'Toutes':
        filtered_data = filtered_data[filtered_data['provstate'] == selected_region]
    
    if selected_attack != 'Tous':
        filtered_data = filtered_data[filtered_data['attacktype1_txt'] == selected_attack]

    # Carte interactive de la France
    st.subheader("🗺️ Localisation des Incidents")
    
    # Données avec coordonnées
    map_data = filtered_data[
        filtered_data['latitude'].notna() & 
        filtered_data['longitude'].notna()
    ].copy()
    
    if len(map_data) > 0:
        # Créer des infobulles détaillées
        map_data['hover_text'] = map_data.apply(lambda row: 
            f"<b>{row['city']}, {row['provstate']}</b><br>" +
            f"📅 {row['iyear']}<br>" +
            f"🎯 {row['attacktype1_txt']}<br>" +
            f"🏢 Cible: {row['targtype1_txt']}<br>" +
            f"💀 Victimes: {int(row['nkill'])}<br>" +
            f"🏥 Blessés: {int(row['nwound'])}<br>" +
            f"👥 Groupe: {row['gname']}"
        , axis=1)
        
        # Créer la carte
        fig_map = px.scatter_mapbox(
            map_data,
            lat="latitude",
            lon="longitude",
            color="attacktype1_txt",
            size="nkill",
            size_max=20,
            hover_name="city",
            hover_data={
                'latitude': False,
                'longitude': False,
                'attacktype1_txt': True,
                'iyear': True,
                'nkill': True,
                'nwound': True
            },
            mapbox_style="open-street-map",
            zoom=5,
            center={"lat": 46.8182, "lon": 2.2137},  # Centre de la France
            height=600,
            title="Incidents Terroristes en France"
        )
        
        fig_map.update_layout(
            mapbox_style="open-street-map",
            margin={"r":0,"t":50,"l":0,"b":0}
        )
        
        st.plotly_chart(fig_map, use_container_width=True)
        
    else:
        st.warning("Aucune donnée avec coordonnées disponible pour les filtres sélectionnés.")

    # Deux colonnes pour les graphiques
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Évolution Temporelle")
        yearly_data = filtered_data.groupby('iyear').size().reset_index(name='incidents')
        
        fig_timeline = px.line(
            yearly_data, 
            x='iyear', 
            y='incidents',
            title="Nombre d'incidents par année",
            labels={'iyear': 'Année', 'incidents': 'Nombre d\'incidents'}
        )
        fig_timeline.update_traces(line_color='#ff6b6b')
        st.plotly_chart(fig_timeline, use_container_width=True)
    
    with col2:
        st.subheader("🎯 Types d'Attaques")
        attack_counts = filtered_data['attacktype1_txt'].value_counts().head(8)
        
        fig_attacks = px.bar(
            x=attack_counts.values,
            y=attack_counts.index,
            orientation='h',
            title="Types d'attaques les plus fréquents",
            labels={'x': 'Nombre d\'incidents', 'y': 'Type d\'attaque'}
        )
        fig_attacks.update_traces(marker_color='#4ecdc4')
        st.plotly_chart(fig_attacks, use_container_width=True)

    # Trois colonnes pour plus de statistiques
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("🏙️ Villes les Plus Touchées")
        city_counts = filtered_data['city'].value_counts().head(10)
        
        fig_cities = px.bar(
            x=city_counts.values,
            y=city_counts.index,
            orientation='h',
            title="Top 10 des villes",
            color=city_counts.values,
            color_continuous_scale='Reds'
        )
        fig_cities.update_layout(showlegend=False, coloraxis_showscale=False)
        st.plotly_chart(fig_cities, use_container_width=True)
    
    with col2:
        st.subheader("🎪 Types de Cibles")
        target_counts = filtered_data['targtype1_txt'].value_counts().head(8)
        
        fig_targets = px.pie(
            values=target_counts.values,
            names=target_counts.index,
            title="Répartition des types de cibles"
        )
        st.plotly_chart(fig_targets, use_container_width=True)
    
    with col3:
        st.subheader("👥 Groupes Terroristes")
        group_counts = filtered_data[filtered_data['gname'] != 'Unknown']['gname'].value_counts().head(8)
        
        if len(group_counts) > 0:
            fig_groups = px.bar(
                x=group_counts.values,
                y=group_counts.index,
                orientation='h',
                title="Groupes les plus actifs",
                color=group_counts.values,
                color_continuous_scale='Blues'
            )
            fig_groups.update_layout(showlegend=False, coloraxis_showscale=False)
            st.plotly_chart(fig_groups, use_container_width=True)
        else:
            st.info("Données de groupes non disponibles pour la sélection actuelle")

    # Tableau détaillé des incidents récents
    st.subheader("📋 Incidents Récents Détaillés")
    
    # Sélectionner les colonnes importantes
    display_columns = ['iyear', 'imonth', 'iday', 'city', 'provstate', 'attacktype1_txt', 
                      'targtype1_txt', 'gname', 'nkill', 'nwound', 'summary']
    
    recent_data = filtered_data.sort_values('iyear', ascending=False).head(20)
    
    # Renommer les colonnes pour l'affichage
    display_data = recent_data[display_columns].copy()
    display_data.columns = ['Année', 'Mois', 'Jour', 'Ville', 'Région', 'Type Attaque', 
                           'Type Cible', 'Groupe', 'Victimes', 'Blessés', 'Résumé']
    
    # Formatage pour l'affichage
    display_data['Résumé'] = display_data['Résumé'].fillna('Non disponible').apply(
        lambda x: x[:100] + "..." if len(str(x)) > 100 else x
    )
    
    st.dataframe(
        display_data,
        use_container_width=True,
        height=400
    )

    # Analyse par décennie
    st.subheader("📈 Analyse par Décennie")
    
    filtered_data['decade'] = (filtered_data['iyear'] // 10) * 10
    decade_stats = filtered_data.groupby('decade').agg({
        'iyear': 'count',
        'nkill': 'sum',
        'nwound': 'sum'
    }).reset_index()
    decade_stats.columns = ['Décennie', 'Incidents', 'Victimes', 'Blessés']
    decade_stats['Décennie'] = decade_stats['Décennie'].astype(str) + 's'
    
    fig_decade = make_subplots(
        rows=1, cols=3,
        subplot_titles=('Incidents par Décennie', 'Victimes par Décennie', 'Blessés par Décennie'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}, {"secondary_y": False}]]
    )
    
    fig_decade.add_trace(
        go.Bar(x=decade_stats['Décennie'], y=decade_stats['Incidents'], 
               name='Incidents', marker_color='#ff6b6b'),
        row=1, col=1
    )
    
    fig_decade.add_trace(
        go.Bar(x=decade_stats['Décennie'], y=decade_stats['Victimes'], 
               name='Victimes', marker_color='#4ecdc4'),
        row=1, col=2
    )
    
    fig_decade.add_trace(
        go.Bar(x=decade_stats['Décennie'], y=decade_stats['Blessés'], 
               name='Blessés', marker_color='#45b7d1'),
        row=1, col=3
    )
    
    fig_decade.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig_decade, use_container_width=True)

else:
    st.error("❌ Impossible de charger les données pour la France")
    st.info("Assurez-vous que le fichier de données est présent et accessible.")