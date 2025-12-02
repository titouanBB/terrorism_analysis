import pandas as pd
import warnings
warnings.filterwarnings('ignore')

# Charger les données
df = pd.read_excel('globalterrorismdb_0522dist.xlsx')

print(f'Taille du dataset: {len(df)} incidents')
print(f'Période: {df["iyear"].min()} - {df["iyear"].max()}')

# Données France
print('\n=== FRANCE ===')
france_data = df[df['country_txt'].str.contains('France', case=False, na=False)]
print(f'Incidents en France: {len(france_data)}')

if len(france_data) > 0:
    print('Années:', sorted(france_data['iyear'].unique()))
    print('\nVilles principales:')
    print(france_data['city'].value_counts().head(10))
    print('\nTypes d\'attaques:')
    print(france_data['attacktype1_txt'].value_counts())
    
    # Coordonnées France
    france_coords = france_data[france_data['latitude'].notna() & france_data['longitude'].notna()]
    print(f'\nAvec coordonnées: {len(france_coords)}/{len(france_data)}')

# Europe
european_countries = ['France', 'Germany', 'United Kingdom', 'Italy', 'Spain', 'Netherlands', 'Belgium', 'Greece', 'Portugal', 'Austria', 'Switzerland', 'Denmark', 'Sweden', 'Norway', 'Finland', 'Ireland', 'Luxembourg', 'Poland', 'Czech Republic', 'Hungary', 'Slovakia', 'Slovenia', 'Croatia', 'Romania', 'Bulgaria', 'Estonia', 'Latvia', 'Lithuania', 'Malta', 'Cyprus']

europe_data = df[df['country_txt'].isin(european_countries)]
print(f'\n=== EUROPE ===')
print(f'Total incidents: {len(europe_data)}')
print('\nPar pays (top 15):')
print(europe_data['country_txt'].value_counts().head(15))

# Colonnes utiles
print('\n=== COLONNES UTILES POUR FRANCE ===')
useful_cols = ['iyear', 'imonth', 'iday', 'country_txt', 'provstate', 'city', 'latitude', 'longitude', 
               'attacktype1_txt', 'targtype1_txt', 'gname', 'weaptype1_txt', 'nkill', 'nwound', 
               'summary', 'motive']
print('Colonnes sélectionnées:', len(useful_cols))

if len(france_data) > 0:
    print('\nExemples d\'incidents en France:')
    for idx, row in france_data.head(3).iterrows():
        print(f"\n{row['iyear']}: {row['city']} - {row['attacktype1_txt']}")
        if pd.notna(row['summary']):
            print(f"  Résumé: {row['summary'][:100]}...")
