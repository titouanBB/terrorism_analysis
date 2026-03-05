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
    page_title="Analyse Terrorisme France",
    page_icon="🇫🇷",
    layout="wide"
)

@st.cache_data
def load_data():
    """Charge les données depuis le fichier Excel"""
    try:
        df = pd.read_excel('../globalterrorismdb_0522dist.xlsx')
        df = df.dropna(subset=['iyear', 'country_txt'])
        return df
    except:
        try:
            df = pd.read_excel('globalterrorismdb_0522dist.xlsx')
            df = df.dropna(subset=['iyear', 'country_txt'])
            return df
        except Exception as e:
            st.error(f"Erreur lors du chargement des données: {e}")
            return None

def main():
    st.title("🇫🇷 Analyse Détaillée du Terrorisme en France")
    st.markdown("### Données précises sur les incidents terroristes en France")
    
    # Chargement des données
    df = load_data()
    if df is None:
        st.stop()
    
    # Filtrer uniquement la France
    france_data = df[df['country_txt'].str.contains('France', case=False, na=False)]
    
    if len(france_data) == 0:
        st.warning("Aucun incident trouvé pour la France dans la base de données.")
        st.stop()
    
    # Sidebar pour les filtres
    st.sidebar.header("🔍 Filtres France")
    
    # Filtre par année
    min_year = int(france_data['iyear'].min())
    max_year = int(france_data['iyear'].max())
    year_range = st.sidebar.slider(
        "Période",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year),
        step=1
    )
    
    # Filtre par ville
    cities = sorted(france_data['city'].dropna().unique())
    selected_cities = st.sidebar.multiselect(
        "Villes",
        options=cities,
        default=cities[:5] if len(cities) > 5 else cities
    )
    
    # Filtre par type d'attaque
    attack_types = sorted(france_data['attacktype1_txt'].dropna().unique())
    selected_attacks = st.sidebar.multiselect(
        "Types d'attaque",
        options=attack_types,
        default=attack_types
    )
    
    # Appliquer les filtres
    filtered_france = france_data[
        (france_data['iyear'] >= year_range[0]) & 
        (france_data['iyear'] <= year_range[1])
    ]
    
    if selected_cities:
        filtered_france = filtered_france[filtered_france['city'].isin(selected_cities)]
    
    if selected_attacks:
        filtered_france = filtered_france[filtered_france['attacktype1_txt'].isin(selected_attacks)]
    
    if len(filtered_france) == 0:
        st.warning("Aucun incident trouvé avec les filtres sélectionnés.")
        st.stop()
    
    # Métriques principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total incidents France", f"{len(filtered_france):,}")
    
    with col2:
        total_killed = filtered_france['nkill'].fillna(0).sum()
        st.metric("Victimes décédées", f"{int(total_killed):,}")
    
    with col3:
        total_wounded = filtered_france['nwound'].fillna(0).sum()
        st.metric("Victimes blessées", f"{int(total_wounded):,}")
    
    with col4:
        cities_count = filtered_france['city'].nunique()
        st.metric("Villes touchées", f"{cities_count}")
    
    # Informations générales sur la France
    st.header("📊 Vue d'ensemble - France")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Évolution temporelle
        yearly_counts = filtered_france.groupby('iyear').size().reset_index(name='incidents')
        
        fig_timeline = px.line(
            yearly_counts, 
            x='iyear', 
            y='incidents',
            title="Évolution des incidents en France par année",
            labels={'iyear': 'Année', 'incidents': 'Nombre d\'incidents'}
        )
        fig_timeline.update_layout(height=400)
        st.plotly_chart(fig_timeline, use_container_width=True)
    
    with col2:
        # Répartition par type d'attaque
        attack_counts = filtered_france['attacktype1_txt'].value_counts()
        
        fig_attacks = px.pie(
            values=attack_counts.values,
            names=attack_counts.index,
            title="Types d'attaques en France"
        )
        fig_attacks.update_layout(height=400)
        st.plotly_chart(fig_attacks, use_container_width=True)
    
    # Analyse géographique détaillée
    st.header("🗺️ Répartition géographique en France")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Top villes
        city_counts = filtered_france['city'].value_counts().head(10)
        
        if len(city_counts) > 0:
            fig_cities = px.bar(
                x=city_counts.values,
                y=city_counts.index,
                orientation='h',
                title="Top 10 des villes les plus touchées",
                labels={'x': 'Nombre d\'incidents', 'y': 'Ville'}
            )
            fig_cities.update_layout(height=400, yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig_cities, use_container_width=True)
    
    with col2:
        # Répartition par région/département
        if 'provstate' in filtered_france.columns:
            region_counts = filtered_france['provstate'].value_counts().head(10)
            
            if len(region_counts) > 0:
                fig_regions = px.bar(
                    x=region_counts.values,
                    y=region_counts.index,
                    orientation='h',
                    title="Top 10 des régions/départements",
                    labels={'x': 'Nombre d\'incidents', 'y': 'Région/Département'}
                )
                fig_regions.update_layout(height=400, yaxis={'categoryorder': 'total ascending'})
                st.plotly_chart(fig_regions, use_container_width=True)
    
    # Carte des incidents si coordonnées disponibles
    if 'latitude' in filtered_france.columns and 'longitude' in filtered_france.columns:
        map_data = filtered_france[['latitude', 'longitude', 'city', 'iyear', 'attacktype1_txt', 'summary']].dropna(subset=['latitude', 'longitude'])
        
        if len(map_data) > 0:
            st.subheader("Localisation des incidents en France")
            
            fig_map = px.scatter_mapbox(
                map_data,
                lat='latitude',
                lon='longitude',
                hover_name='city',
                hover_data=['iyear', 'attacktype1_txt'],
                zoom=5,
                height=500,
                title="Carte des incidents terroristes en France"
            )
            fig_map.update_layout(mapbox_style="open-street-map")
            st.plotly_chart(fig_map, use_container_width=True)
    
    # Analyse temporelle détaillée
    st.header("📅 Analyse temporelle détaillée")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Distribution par mois
        month_counts = filtered_france['imonth'].value_counts().sort_index()
        month_names = {1: 'Jan', 2: 'Fév', 3: 'Mar', 4: 'Avr', 5: 'Mai', 6: 'Jun',
                      7: 'Jul', 8: 'Aoû', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Déc'}
        
        if len(month_counts) > 0:
            fig_months = px.bar(
                x=[month_names.get(month, month) for month in month_counts.index],
                y=month_counts.values,
                title="Distribution des incidents par mois",
                labels={'x': 'Mois', 'y': 'Nombre d\'incidents'}
            )
            fig_months.update_layout(height=400)
            st.plotly_chart(fig_months, use_container_width=True)
    
    with col2:
        # Groupes terroristes
        if 'gname' in filtered_france.columns:
            group_counts = filtered_france['gname'].value_counts().head(10)
            group_counts = group_counts[group_counts.index != 'Unknown']  # Exclure "Unknown"
            
            if len(group_counts) > 0:
                fig_groups = px.bar(
                    x=group_counts.values,
                    y=group_counts.index,
                    orientation='h',
                    title="Groupes terroristes les plus actifs",
                    labels={'x': 'Nombre d\'incidents', 'y': 'Groupe'}
                )
                fig_groups.update_layout(height=400, yaxis={'categoryorder': 'total ascending'})
                st.plotly_chart(fig_groups, use_container_width=True)
    
    # SECTION DÉTAILLÉE: GROUPES TERRORISTES EN FRANCE
    st.header("🎭 Analyse approfondie des groupes terroristes en France")
    
    if 'gname' in filtered_france.columns:
        # Statistiques globales des groupes
        st.subheader("📊 Vue d'ensemble des groupes terroristes")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_groups = filtered_france['gname'].nunique()
            st.metric("Groupes identifiés", f"{total_groups}")
        
        with col2:
            unknown_count = len(filtered_france[filtered_france['gname'] == 'Unknown'])
            unknown_percent = (unknown_count / len(filtered_france) * 100) if len(filtered_france) > 0 else 0
            st.metric("Attaques non-attribuées", f"{unknown_count} ({unknown_percent:.1f}%)")
        
        with col3:
            known_attacks = len(filtered_france[filtered_france['gname'] != 'Unknown'])
            st.metric("Attaques attribuées", f"{known_attacks}")
        
        with col4:
            # Groupe le plus meurtrier
            group_kills = filtered_france.groupby('gname')['nkill'].sum().fillna(0)
            group_kills = group_kills[group_kills.index != 'Unknown']
            if len(group_kills) > 0:
                deadliest = group_kills.idxmax()
                deadliest_count = int(group_kills.max())
                st.metric("Groupe le plus meurtrier", f"{deadliest_count} victimes")
                st.caption(f"{deadliest}")
        
        # Top 15 des groupes terroristes
        st.subheader("🏆 Top 15 des groupes terroristes en France")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Graphique avec le TOP 15
            all_groups = filtered_france['gname'].value_counts().head(15)
            
            fig_top_groups = px.bar(
                x=all_groups.values,
                y=all_groups.index,
                orientation='h',
                title="Top 15 des groupes par nombre d'incidents",
                labels={'x': 'Nombre d\'incidents', 'y': 'Groupe terroriste'},
                color=all_groups.values,
                color_continuous_scale='Reds'
            )
            fig_top_groups.update_layout(
                height=600,
                yaxis={'categoryorder': 'total ascending'},
                showlegend=False
            )
            st.plotly_chart(fig_top_groups, use_container_width=True)
        
        with col2:
            st.markdown("#### Statistiques détaillées")
            
            # Tableau des top groupes avec statistiques
            group_stats = filtered_france.groupby('gname').agg({
                'eventid': 'count',
                'nkill': lambda x: int(x.fillna(0).sum()),
                'nwound': lambda x: int(x.fillna(0).sum()),
                'iyear': ['min', 'max']
            }).round(0)
            
            group_stats.columns = ['Incidents', 'Tués', 'Blessés', 'Début', 'Fin']
            group_stats = group_stats.sort_values('Incidents', ascending=False).head(15)
            group_stats['Période'] = group_stats['Fin'] - group_stats['Début']
            
            st.dataframe(
                group_stats,
                use_container_width=True,
                height=600
            )
        
        # FOCUS SPÉCIAL: ACTION DIRECTE
        st.markdown("---")
        st.subheader("🎯 Focus spécial: Action Directe")
        
        action_directe = filtered_france[
            filtered_france['gname'].str.contains('Action Directe', case=False, na=False) |
            filtered_france['gname'].str.contains('Direct Action', case=False, na=False)
        ]
        
        if len(action_directe) > 0:
            st.markdown("""
            **Action Directe** est une organisation terroriste d'extrême gauche française, active principalement dans les années 1980. 
            Ce groupe a mené de nombreuses actions contre des cibles gouvernementales, militaires et économiques.
            """)
            
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                st.metric("Total incidents", f"{len(action_directe)}")
            
            with col2:
                ad_killed = int(action_directe['nkill'].fillna(0).sum())
                st.metric("Victimes tuées", f"{ad_killed}")
            
            with col3:
                ad_wounded = int(action_directe['nwound'].fillna(0).sum())
                st.metric("Victimes blessées", f"{ad_wounded}")
            
            with col4:
                ad_start = int(action_directe['iyear'].min())
                ad_end = int(action_directe['iyear'].max())
                st.metric("Période active", f"{ad_start}-{ad_end}")
            
            with col5:
                ad_duration = ad_end - ad_start + 1
                st.metric("Années d'activité", f"{ad_duration} ans")
            
            # Visualisations Action Directe
            col1, col2 = st.columns(2)
            
            with col1:
                # Évolution temporelle d'Action Directe
                ad_timeline = action_directe.groupby('iyear').size().reset_index(name='incidents')
                
                fig_ad_timeline = px.line(
                    ad_timeline,
                    x='iyear',
                    y='incidents',
                    title="Évolution des attaques d'Action Directe par année",
                    labels={'iyear': 'Année', 'incidents': 'Nombre d\'incidents'},
                    markers=True
                )
                fig_ad_timeline.update_traces(line_color='#DC143C', marker=dict(size=10))
                fig_ad_timeline.update_layout(height=400)
                st.plotly_chart(fig_ad_timeline, use_container_width=True)
            
            with col2:
                # Types de cibles d'Action Directe
                if 'targtype1_txt' in action_directe.columns:
                    ad_targets = action_directe['targtype1_txt'].value_counts()
                    
                    fig_ad_targets = px.pie(
                        values=ad_targets.values,
                        names=ad_targets.index,
                        title="Types de cibles d'Action Directe"
                    )
                    fig_ad_targets.update_layout(height=400)
                    st.plotly_chart(fig_ad_targets, use_container_width=True)
            
            # Villes ciblées par Action Directe
            col1, col2 = st.columns(2)
            
            with col1:
                ad_cities = action_directe['city'].value_counts().head(10)
                
                fig_ad_cities = px.bar(
                    x=ad_cities.values,
                    y=ad_cities.index,
                    orientation='h',
                    title="Villes ciblées par Action Directe",
                    labels={'x': 'Nombre d\'incidents', 'y': 'Ville'}
                )
                fig_ad_cities.update_layout(height=400, yaxis={'categoryorder': 'total ascending'})
                st.plotly_chart(fig_ad_cities, use_container_width=True)
            
            with col2:
                # Types d'attaques d'Action Directe
                ad_attacks = action_directe['attacktype1_txt'].value_counts()
                
                fig_ad_attacks = px.bar(
                    x=ad_attacks.values,
                    y=ad_attacks.index,
                    orientation='h',
                    title="Types d'attaques d'Action Directe",
                    labels={'x': 'Nombre d\'incidents', 'y': 'Type d\'attaque'}
                )
                fig_ad_attacks.update_layout(height=400, yaxis={'categoryorder': 'total ascending'})
                st.plotly_chart(fig_ad_attacks, use_container_width=True)
            
            # Liste détaillée des incidents d'Action Directe
            st.markdown("#### 📋 Liste détaillée des incidents d'Action Directe")
            
            ad_display_columns = [
                'iyear', 'imonth', 'iday', 'city', 'provstate',
                'attacktype1_txt', 'targtype1_txt', 'weaptype1_txt',
                'nkill', 'nwound', 'summary'
            ]
            
            ad_available_columns = [col for col in ad_display_columns if col in action_directe.columns]
            
            ad_display_df = action_directe[ad_available_columns].copy()
            ad_display_df = ad_display_df.rename(columns={
                'iyear': 'Année',
                'imonth': 'Mois',
                'iday': 'Jour',
                'city': 'Ville',
                'provstate': 'Région',
                'attacktype1_txt': 'Type d\'attaque',
                'targtype1_txt': 'Type de cible',
                'weaptype1_txt': 'Type d\'arme',
                'nkill': 'Tués',
                'nwound': 'Blessés',
                'summary': 'Résumé'
            })
            
            st.dataframe(
                ad_display_df.sort_values('Année', ascending=False),
                use_container_width=True,
                height=400
            )
        else:
            st.info("Aucun incident attribué à Action Directe dans les données filtrées.")
        
        # Comparaison des principaux groupes
        st.markdown("---")
        st.subheader("⚔️ Comparaison des principaux groupes terroristes")
        
        # Top 5 groupes (excluant Unknown)
        top_groups = filtered_france[filtered_france['gname'] != 'Unknown']['gname'].value_counts().head(5).index.tolist()
        
        if len(top_groups) > 0:
            # Évolution temporelle comparative
            comparison_data = []
            
            for group in top_groups:
                group_data = filtered_france[filtered_france['gname'] == group]
                group_timeline = group_data.groupby('iyear').size().reset_index(name='incidents')
                group_timeline['groupe'] = group
                comparison_data.append(group_timeline)
            
            if comparison_data:
                comparison_df = pd.concat(comparison_data, ignore_index=True)
                
                fig_comparison = px.line(
                    comparison_df,
                    x='iyear',
                    y='incidents',
                    color='groupe',
                    title="Évolution comparative des 5 principaux groupes terroristes",
                    labels={'iyear': 'Année', 'incidents': 'Nombre d\'incidents', 'groupe': 'Groupe'},
                    markers=True
                )
                fig_comparison.update_layout(height=500, hovermode='x unified')
                st.plotly_chart(fig_comparison, use_container_width=True)
            
            # Tableau comparatif
            st.markdown("#### 📊 Tableau comparatif détaillé")
            
            comparison_stats = []
            
            for group in top_groups:
                group_data = filtered_france[filtered_france['gname'] == group]
                
                stats = {
                    'Groupe': group,
                    'Incidents': len(group_data),
                    'Tués': int(group_data['nkill'].fillna(0).sum()),
                    'Blessés': int(group_data['nwound'].fillna(0).sum()),
                    'Début': int(group_data['iyear'].min()),
                    'Fin': int(group_data['iyear'].max()),
                    'Létalité moyenne': round(group_data['nkill'].fillna(0).mean(), 2),
                    'Villes ciblées': group_data['city'].nunique()
                }
                
                comparison_stats.append(stats)
            
            comparison_df_stats = pd.DataFrame(comparison_stats)
            comparison_df_stats = comparison_df_stats.set_index('Groupe')
            
            st.dataframe(
                comparison_df_stats,
                use_container_width=True
            )
    
    # Analyse des cibles et armes
    st.header("🎯 Analyse des cibles et moyens")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Types de cibles
        if 'targtype1_txt' in filtered_france.columns:
            target_counts = filtered_france['targtype1_txt'].value_counts().head(8)
            
            fig_targets = px.pie(
                values=target_counts.values,
                names=target_counts.index,
                title="Types de cibles visées"
            )
            fig_targets.update_layout(height=400)
            st.plotly_chart(fig_targets, use_container_width=True)
    
    with col2:
        # Types d'armes
        if 'weaptype1_txt' in filtered_france.columns:
            weapon_counts = filtered_france['weaptype1_txt'].value_counts().head(8)
            
            fig_weapons = px.pie(
                values=weapon_counts.values,
                names=weapon_counts.index,
                title="Types d'armes utilisées"
            )
            fig_weapons.update_layout(height=400)
            st.plotly_chart(fig_weapons, use_container_width=True)
    
    # Données détaillées
    st.header("📋 Incidents détaillés en France")
    
    # Colonnes importantes pour l'affichage
    display_columns = [
        'iyear', 'imonth', 'iday', 'city', 'provstate',
        'attacktype1_txt', 'targtype1_txt', 'weaptype1_txt', 
        'gname', 'nkill', 'nwound', 'summary'
    ]
    
    available_columns = [col for col in display_columns if col in filtered_france.columns]
    
    # Renommer les colonnes pour l'affichage
    column_names = {
        'iyear': 'Année',
        'imonth': 'Mois', 
        'iday': 'Jour',
        'city': 'Ville',
        'provstate': 'Région/Département',
        'attacktype1_txt': 'Type d\'attaque',
        'targtype1_txt': 'Type de cible',
        'weaptype1_txt': 'Type d\'arme',
        'gname': 'Groupe terroriste',
        'nkill': 'Tués',
        'nwound': 'Blessés',
        'summary': 'Résumé'
    }
    
    display_df = filtered_france[available_columns].copy()
    display_df = display_df.rename(columns=column_names)
    
    st.dataframe(
        display_df,
        use_container_width=True,
        height=400
    )
    
    # Statistiques finales
    st.header("📈 Statistiques France")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("Période d'activité")
        st.write(f"**Première attaque:** {filtered_france['iyear'].min()}")
        st.write(f"**Dernière attaque:** {filtered_france['iyear'].max()}")
        st.write(f"**Période couverte:** {filtered_france['iyear'].max() - filtered_france['iyear'].min() + 1} ans")
    
    with col2:
        st.subheader("Bilan humain")
        total_casualties = int(filtered_france['nkill'].fillna(0).sum() + filtered_france['nwound'].fillna(0).sum())
        st.write(f"**Total victimes:** {total_casualties:,}")
        avg_per_incident = total_casualties / len(filtered_france) if len(filtered_france) > 0 else 0
        st.write(f"**Moyenne par incident:** {avg_per_incident:.1f}")
    
    with col3:
        st.subheader("Répartition")
        most_active_year = filtered_france['iyear'].mode().iloc[0] if len(filtered_france) > 0 else "N/A"
        year_count = len(filtered_france[filtered_france['iyear'] == most_active_year]) if most_active_year != "N/A" else 0
        st.write(f"**Année la plus active:** {most_active_year} ({year_count} incidents)")
        most_targeted_city = filtered_france['city'].mode().iloc[0] if len(filtered_france) > 0 else "N/A"
        st.write(f"**Ville la plus touchée:** {most_targeted_city}")
    
    # Option de téléchargement
    st.header("💾 Télécharger les données")
    if st.button("Télécharger les données France (CSV)"):
        csv = filtered_france.to_csv(index=False)
        st.download_button(
            label="Télécharger CSV France",
            data=csv,
            file_name=f"terrorism_france_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    main()