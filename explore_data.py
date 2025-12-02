import pandas as pd
import numpy as np

# Charger le fichier Excel
try:
    df = pd.read_excel('globalterrorismdb_0522dist.xlsx', engine='openpyxl')
    
    print("=== INFORMATIONS SUR LE DATASET ===")
    print(f"Forme du dataset: {df.shape}")
    print(f"Nombre de lignes: {df.shape[0]}")
    print(f"Nombre de colonnes: {df.shape[1]}")
    
    print("\n=== COLONNES DISPONIBLES ===")
    for i, col in enumerate(df.columns):
        print(f"{i+1}. {col}")
    
    print("\n=== PREMIÈRES LIGNES ===")
    print(df.head())
    
    print("\n=== INFORMATIONS SUR LES TYPES DE DONNÉES ===")
    print(df.info())
    
    print("\n=== VALEURS MANQUANTES ===")
    missing_data = df.isnull().sum()
    print(missing_data[missing_data > 0].sort_values(ascending=False))
    
except Exception as e:
    print(f"Erreur lors du chargement du fichier: {e}")
