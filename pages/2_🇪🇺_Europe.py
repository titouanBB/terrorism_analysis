import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Configuration de la page
st.set_page_config(
    page_title="Europe - Analyse Comparative",
    page_icon="🇪🇺",
    layout="wide"
)

# Setup data
from setup_data import setup_data
setup_data()

@st.cache_data
def load_europe_data():
    """Charge les données européennes"""
    try:
        df = pd.read_excel('globalterrorismdb_0522dist.xlsx')
        
        european_countries = [
            'France', 'Germany', 'United Kingdom', 'Italy', 'Spain', 'Netherlands', 
            'Belgium', 'Greece', 'Portugal', 'Austria', 'Switzerland', 'Denmark',
            'Sweden', 'Norway', 'Finland', 'Ireland', 'Luxembourg', 'Poland',
            'Czech Republic', 'Hungary', 'Slovakia', 'Slovenia', 'Croatia',
            'Romania', 'Bulgaria', 'Estonia', 'Latvia', 'Lithuania', 'Malta', 'Cyprus'
        ]
        
        df = df[df['country_txt'].isin(european_countries)].copy()
        df['nkill'] = df['nkill'].fillna(0)
        df['nwound'] = df['nwound'].fillna(0)
        
        return df
    except Exception as e:
        st.error(f"Erreur : {e}")
        return None

st.title("🇪🇺 Analyse Comparative - Europe")
st.markdown("### Comparaison des incidents terroristes par pays européens")
st.markdown("---")

df = load_europe_data()

if df is not None:
    # Métriques globales
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("📊 Total Incidents", f"{len(df):,}")
    with col2:
        st.metric("💀 Total Victimes", f"{int(df['nkill'].sum()):,}")
    with col3:
        st.metric("🏥 Total Blessés", f"{int(df['nwound'].sum()):,}")
    with col4:
        st.metric("🗺️ Pays Touchés", f"{df['country_txt'].nunique()}")
    with col5:
        period = f"{df['iyear'].min()}-{df['iyear'].max()}"
        st.metric("📅 Période", period)
    
    st.markdown("---")
    
    # Sidebar pour les filtres
    with st.sidebar:
        st.header("🔍 Filtres Globaux")
        
        # Filtre années
        years = sorted(df['iyear'].unique())
        year_range = st.select_slider(
            "Période d'analyse",
            options=years,
            value=(years[0], years[-1])
        )
        
        # Filtre pays
        all_countries = sorted(df['country_txt'].unique())
        selected_countries = st.multiselect(
            "Pays à analyser",
            all_countries,
            default=all_countries[:10]  # Top 10 par défaut
        )
        
        if not selected_countries:
            selected_countries = all_countries[:5]  # Au moins 5 pays
    
    # Filtrer les données
    filtered_df = df[
        (df['iyear'] >= year_range[0]) & 
        (df['iyear'] <= year_range[1]) &
        (df['country_txt'].isin(selected_countries))
    ]
    
    # Vue d'ensemble par pays
    st.subheader("📊 Vue d'Ensemble par Pays")
    
    # Statistiques par pays
    country_stats = filtered_df.groupby('country_txt').agg({
        'iyear': 'count',
        'nkill': 'sum',
        'nwound': 'sum'
    }).reset_index()
    country_stats.columns = ['Pays', 'Incidents', 'Victimes', 'Blessés']
    country_stats = country_stats.sort_values('Incidents', ascending=False)
    
    # Graphiques comparatifs
    col1, col2 = st.columns(2)
    
    with col1:
        # Incidents par pays
        fig1 = px.bar(
            country_stats.head(15), 
            x='Incidents', 
            y='Pays',
            orientation='h',
            title="Nombre d'incidents par pays",
            color='Incidents',
            color_continuous_scale='Reds'
        )
        fig1.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        # Victimes par pays
        fig2 = px.bar(
            country_stats.head(15), 
            x='Victimes', 
            y='Pays',
            orientation='h',
            title="Nombre de victimes par pays",
            color='Victimes',
            color_continuous_scale='Blues'
        )
        fig2.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig2, use_container_width=True)
    
    # Évolution temporelle
    st.subheader("📈 Évolution Temporelle")
    
    # Timeline par pays
    timeline_data = filtered_df.groupby(['iyear', 'country_txt']).size().reset_index(name='incidents')
    
    # Top 5 pays pour la timeline
    top_countries = country_stats.head(5)['Pays'].tolist()
    timeline_filtered = timeline_data[timeline_data['country_txt'].isin(top_countries)]
    
    fig_timeline = px.line(
        timeline_filtered,
        x='iyear',
        y='incidents',
        color='country_txt',
        title=f"Évolution des incidents (Top 5 pays)",
        labels={'iyear': 'Année', 'incidents': 'Nombre d\'incidents', 'country_txt': 'Pays'}
    )
    st.plotly_chart(fig_timeline, use_container_width=True)
    
    # Heatmap par décennie
    filtered_df['decade'] = (filtered_df['iyear'] // 10) * 10
    decade_country = filtered_df.groupby(['decade', 'country_txt']).size().reset_index(name='incidents')
    decade_pivot = decade_country.pivot(index='country_txt', columns='decade', values='incidents').fillna(0)
    
    if not decade_pivot.empty:
        fig_heatmap = px.imshow(
            decade_pivot.values,
            x=[f"{int(col)}s" for col in decade_pivot.columns],
            y=decade_pivot.index,
            title="Heatmap des incidents par pays et décennie",
            aspect='auto',
            color_continuous_scale='Reds'
        )
        fig_heatmap.update_layout(height=max(400, len(decade_pivot.index) * 20))
        st.plotly_chart(fig_heatmap, use_container_width=True)
    
    # Analyses par type
    st.subheader("🎯 Analyses par Catégories")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Types d'Attaques**")
        attack_types = filtered_df['attacktype1_txt'].value_counts().head(10)
        fig_attacks = px.pie(
            values=attack_types.values,
            names=attack_types.index,
            title="Types d'attaques"
        )
        st.plotly_chart(fig_attacks, use_container_width=True)
    
    with col2:
        st.markdown("**Types de Cibles**")
        target_types = filtered_df['targtype1_txt'].value_counts().head(10)
        fig_targets = px.pie(
            values=target_types.values,
            names=target_types.index,
            title="Types de cibles"
        )
        st.plotly_chart(fig_targets, use_container_width=True)
    
    with col3:
        st.markdown("**Groupes Terroristes**")
        groups = filtered_df[filtered_df['gname'] != 'Unknown']['gname'].value_counts().head(10)
        if len(groups) > 0:
            fig_groups = px.bar(
                x=groups.values,
                y=groups.index,
                orientation='h',
                title="Principaux groupes"
            )
            st.plotly_chart(fig_groups, use_container_width=True)
        else:
            st.info("Données de groupes limitées")
    
    # Tableau comparatif détaillé
    st.subheader("📋 Tableau Comparatif Détaillé")
    
    # Statistiques avancées par pays
    detailed_stats = filtered_df.groupby('country_txt').agg({
        'iyear': ['count', 'min', 'max'],
        'nkill': ['sum', 'mean'],
        'nwound': ['sum', 'mean'],
        'attacktype1_txt': lambda x: x.value_counts().index[0] if len(x) > 0 else 'Unknown'
    }).round(2)
    
    # Aplatir les colonnes multi-niveau
    detailed_stats.columns = [
        'Total_Incidents', 'Première_Année', 'Dernière_Année',
        'Total_Victimes', 'Moy_Victimes_par_Incident',
        'Total_Blessés', 'Moy_Blessés_par_Incident',
        'Type_Attaque_Principal'
    ]
    
    detailed_stats = detailed_stats.sort_values('Total_Incidents', ascending=False)
    
    # Reformater pour l'affichage
    display_stats = detailed_stats.copy()
    display_stats['Période_Activité'] = display_stats['Première_Année'].astype(int).astype(str) + '-' + display_stats['Dernière_Année'].astype(int).astype(str)
    display_stats = display_stats.drop(['Première_Année', 'Dernière_Année'], axis=1)
    
    # Réorganiser les colonnes
    column_order = ['Total_Incidents', 'Période_Activité', 'Total_Victimes', 'Total_Blessés', 
                   'Moy_Victimes_par_Incident', 'Moy_Blessés_par_Incident', 'Type_Attaque_Principal']
    display_stats = display_stats[column_order]
    
    st.dataframe(display_stats, use_container_width=True, height=400)
    
    # Analyse géographique
    st.subheader("🗺️ Répartition Géographique")
    
    # Créer une carte si des coordonnées sont disponibles
    map_data = filtered_df[
        filtered_df['latitude'].notna() & 
        filtered_df['longitude'].notna()
    ]
    
    if len(map_data) > 0:
        # Agrégation par pays pour la carte
        country_coords = map_data.groupby('country_txt').agg({
            'latitude': 'mean',
            'longitude': 'mean',
            'iyear': 'count',
            'nkill': 'sum'
        }).reset_index()
        country_coords.columns = ['Pays', 'Latitude', 'Longitude', 'Incidents', 'Victimes']
        
        fig_map = px.scatter_mapbox(
            country_coords,
            lat='Latitude',
            lon='Longitude',
            size='Incidents',
            color='Victimes',
            hover_name='Pays',
            hover_data=['Incidents', 'Victimes'],
            title="Répartition des incidents en Europe",
            mapbox_style="open-street-map",
            height=600,
            zoom=3,
            center={"lat": 54, "lon": 15}
        )
        
        st.plotly_chart(fig_map, use_container_width=True)
    else:
        st.info("Données géographiques insuffisantes pour afficher la carte")

else:
    st.error("❌ Impossible de charger les données européennes")