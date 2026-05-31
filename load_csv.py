import pandas as pd
import sys

# Forcer l'encodage UTF-8 pour Windows
sys.stdout.reconfigure(encoding='utf-8')

# Chargement du fichier CSV
df = pd.read_csv("data/source.csv")

print("=== Apercu des donnees ===")
print(df.head())

print("\n=== Types des colonnes ===")
print(df.dtypes)

print("\n=== Statistiques de base ===")
print(df.describe())

print("\n=== Valeurs manquantes ===")
print(df.isnull().sum())

# Validation simple
nb_manquants = df.isnull().sum().sum()
if nb_manquants > 0:
    print(f"\nATTENTION : {nb_manquants} valeur(s) manquante(s) detectee(s)")
else:
    print("\nOK : Aucune valeur manquante")