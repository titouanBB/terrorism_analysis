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
    page_title="Analyse du Terrorisme Mondial",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Cache pour charger les données
@st.cache_data
def load_data():
    """Charge les données depuis le fichier Excel ou ZIP"""
    try:
        # Essayer de charger le .xlsx directement
        df = pd.read_excel('globalterrorismdb_0522dist.xlsx')
        df = df.dropna(subset=['iyear', 'country_txt'])
        return df
    except:
        try:
            # Essayer de charger depuis le .zip (pour GitHub/déploiement)
            import zipfile
            with zipfile.ZipFile('globalterrorismdb_0522dist.zip', 'r') as zip_ref:
                with zip_ref.open('globalterrorismdb_0522dist.xlsx') as excel_file:
                    df = pd.read_excel(excel_file)
                    df = df.dropna(subset=['iyear', 'country_txt'])
                    return df
        except Exception as e:
            st.error(f"Erreur lors du chargement des données: {e}")
            return None

def main():
    st.title("🌍 Analyse du Terrorisme Mondial")
    st.markdown("### Exploration interactive de la Global Terrorism Database")
    
    # Chargement des données
    df = load_data()
    if df is None:
        st.stop()
    
    # Sidebar pour les filtres
    st.sidebar.header("🔍 Filtres")
    
    # Filtre par année
    min_year = int(df['iyear'].min())
    max_year = int(df['iyear'].max())
    year_range = st.sidebar.slider(
        "Période",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year),
        step=1
    )
    
    # Filtre par pays
    countries = sorted(df['country_txt'].dropna().unique())
    selected_country = st.sidebar.selectbox(
        "Pays (optionnel)",
        options=["Tous les pays"] + countries,
        index=0
    )
    
    # Filtre par région
    regions = sorted(df['region_txt'].dropna().unique())
    selected_regions = st.sidebar.multiselect(
        "Régions",
        options=regions,
        default=regions[:5]  # Sélectionne les 5 premières par défaut
    )
    
    # Filtre par type d'attaque
    attack_types = sorted(df['attacktype1_txt'].dropna().unique())
    selected_attacks = st.sidebar.multiselect(
        "Types d'attaque",
        options=attack_types,
        default=attack_types[:3]
    )
    
    # Appliquer les filtres
    filtered_df = df[
        (df['iyear'] >= year_range[0]) & 
        (df['iyear'] <= year_range[1])
    ]
    
    # Filtre par pays spécifique
    if selected_country != "Tous les pays":
        filtered_df = filtered_df[filtered_df['country_txt'] == selected_country]
    
    if selected_regions:
        filtered_df = filtered_df[filtered_df['region_txt'].isin(selected_regions)]
    
    if selected_attacks:
        filtered_df = filtered_df[filtered_df['attacktype1_txt'].isin(selected_attacks)]
    
    # Vérification si des données existent après filtrage
    if len(filtered_df) == 0:
        st.warning("⚠️ Aucun incident trouvé avec les filtres sélectionnés.")
        
        if selected_country != "Tous les pays":
            st.info(f"📊 Le pays **{selected_country}** n'a pas d'incidents terroristes enregistrés dans la période sélectionnée ({year_range[0]} - {year_range[1]}) ou avec les filtres appliqués.")
            
            # Vérifier si le pays a des incidents dans toute la base
            country_total = df[df['country_txt'] == selected_country]
            if len(country_total) > 0:
                st.info(f"💡 **{selected_country}** a {len(country_total)} incident(s) au total dans la base de données (toutes années confondues), mais aucun ne correspond aux filtres actuels.")
            else:
                st.success(f"✅ **{selected_country}** n'a aucun incident terroriste enregistré dans cette base de données, ce qui est une bonne nouvelle !")
        
        st.markdown("**Suggestions :**")
        st.markdown("- Élargissez la période temporelle")
        st.markdown("- Supprimez certains filtres (régions, types d'attaques)")
        st.markdown("- Sélectionnez un autre pays")
        st.stop()
    
    # Métriques principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total des incidents",
            f"{len(filtered_df):,}",
            delta=f"{len(filtered_df) - len(df):,}"
        )
    
    with col2:
        total_killed = filtered_df['nkill'].sum() if 'nkill' in filtered_df.columns else 0
        st.metric("Victimes décédées", f"{int(total_killed):,}")
    
    with col3:
        total_wounded = filtered_df['nwound'].sum() if 'nwound' in filtered_df.columns else 0
        st.metric("Victimes blessées", f"{int(total_wounded):,}")
    
    with col4:
        countries_count = filtered_df['country_txt'].nunique()
        st.metric("Pays affectés", f"{countries_count}")
    
    # Onglets pour différentes visualisations
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Tendances temporelles", 
        "🗺️ Répartition géographique", 
        "⚔️ Types d'attaques", 
        "🎯 Cibles", 
        "📋 Données détaillées"
    ])
    
    with tab1:
        st.header("Évolution temporelle des incidents")
        
        # Graphique des incidents par année
        yearly_counts = filtered_df.groupby('iyear').size().reset_index(name='incidents')
        
        fig_timeline = px.line(
            yearly_counts, 
            x='iyear', 
            y='incidents',
            title="Nombre d'incidents terroristes par année",
            labels={'iyear': 'Année', 'incidents': 'Nombre d\'incidents'}
        )
        fig_timeline.update_layout(height=500)
        st.plotly_chart(fig_timeline, use_container_width=True)
        
        # Heatmap par mois et année
        if len(filtered_df) > 0:
            monthly_data = filtered_df.groupby(['iyear', 'imonth']).size().reset_index(name='incidents')
            monthly_pivot = monthly_data.pivot(index='iyear', columns='imonth', values='incidents').fillna(0)
            
            fig_heatmap = px.imshow(
                monthly_pivot,
                title="Distribution des incidents par mois et année",
                labels=dict(x="Mois", y="Année", color="Incidents"),
                aspect="auto"
            )
            st.plotly_chart(fig_heatmap, use_container_width=True)
    
    with tab2:
        st.header("Répartition géographique")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Top pays
            country_counts = filtered_df['country_txt'].value_counts().head(15)
            
            fig_countries = px.bar(
                x=country_counts.values,
                y=country_counts.index,
                orientation='h',
                title="Top 15 des pays les plus touchés",
                labels={'x': 'Nombre d\'incidents', 'y': 'Pays'}
            )
            fig_countries.update_layout(height=500, yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig_countries, use_container_width=True)
        
        with col2:
            # Top régions
            region_counts = filtered_df['region_txt'].value_counts()
            
            fig_regions = px.pie(
                values=region_counts.values,
                names=region_counts.index,
                title="Distribution par région"
            )
            fig_regions.update_layout(height=500)
            st.plotly_chart(fig_regions, use_container_width=True)
        
        # Carte mondiale si les coordonnées sont disponibles
        if 'latitude' in filtered_df.columns and 'longitude' in filtered_df.columns:
            map_data = filtered_df[['latitude', 'longitude', 'country_txt', 'city', 'iyear', 'attacktype1_txt']].dropna()
            if len(map_data) > 0:
                st.subheader("Carte des incidents")
                
                fig_map = px.scatter_mapbox(
                    map_data.head(1000),  # Limite pour les performances
                    lat='latitude',
                    lon='longitude',
                    hover_name='city',
                    hover_data=['country_txt', 'iyear', 'attacktype1_txt'],
                    zoom=1,
                    height=600,
                    title="Localisation des incidents (1000 premiers points)"
                )
                fig_map.update_layout(mapbox_style="open-street-map")
                st.plotly_chart(fig_map, use_container_width=True)
    
    with tab3:
        st.header("Types d'attaques")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Types d'attaques
            attack_counts = filtered_df['attacktype1_txt'].value_counts()
            
            fig_attacks = px.bar(
                x=attack_counts.values,
                y=attack_counts.index,
                orientation='h',
                title="Types d'attaques les plus fréquents",
                labels={'x': 'Nombre d\'incidents', 'y': 'Type d\'attaque'}
            )
            fig_attacks.update_layout(height=500, yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig_attacks, use_container_width=True)
        
        with col2:
            # Types d'armes
            if 'weaptype1_txt' in filtered_df.columns:
                weapon_counts = filtered_df['weaptype1_txt'].value_counts().head(10)
                
                fig_weapons = px.pie(
                    values=weapon_counts.values,
                    names=weapon_counts.index,
                    title="Types d'armes utilisées (Top 10)"
                )
                fig_weapons.update_layout(height=500)
                st.plotly_chart(fig_weapons, use_container_width=True)
    
    with tab4:
        st.header("Analyse des cibles")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Types de cibles
            if 'targtype1_txt' in filtered_df.columns:
                target_counts = filtered_df['targtype1_txt'].value_counts().head(10)
                
                fig_targets = px.bar(
                    x=target_counts.values,
                    y=target_counts.index,
                    orientation='h',
                    title="Types de cibles les plus visées",
                    labels={'x': 'Nombre d\'incidents', 'y': 'Type de cible'}
                )
                fig_targets.update_layout(height=500, yaxis={'categoryorder': 'total ascending'})
                st.plotly_chart(fig_targets, use_container_width=True)
        
        with col2:
            # Succès des attaques
            if 'success' in filtered_df.columns:
                success_counts = filtered_df['success'].value_counts()
                success_labels = {1: 'Succès', 0: 'Échec'}
                
                fig_success = px.pie(
                    values=success_counts.values,
                    names=[success_labels.get(x, f'Inconnu ({x})') for x in success_counts.index],
                    title="Taux de succès des attaques"
                )
                fig_success.update_layout(height=500)
                st.plotly_chart(fig_success, use_container_width=True)
    
    with tab5:
        st.header("Données détaillées")
        
        # Sélection des colonnes à afficher
        display_columns = [
            'iyear', 'imonth', 'iday', 'country_txt', 'region_txt', 'city',
            'attacktype1_txt', 'targtype1_txt', 'weaptype1_txt', 'gname',
            'nkill', 'nwound', 'summary'
        ]
        
        available_columns = [col for col in display_columns if col in filtered_df.columns]
        
        st.subheader(f"Échantillon des données ({len(filtered_df):,} incidents)")
        st.dataframe(
            filtered_df[available_columns].head(1000),
            use_container_width=True
        )
        
        # Option de téléchargement
        if st.button("Télécharger les données filtrées (CSV)"):
            csv = filtered_df.to_csv(index=False)
            st.download_button(
                label="Télécharger CSV",
                data=csv,
                file_name=f"terrorism_data_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )

if __name__ == "__main__":
    main()
