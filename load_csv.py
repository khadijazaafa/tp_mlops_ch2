import pandas as pd

# Chargement du fichier CSV
df = pd.read_csv("data/source.csv")

print("=== Aperçu des données ===")
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
    print(f"\n⚠️  Attention : {nb_manquants} valeur(s) manquante(s) détectée(s)")
else:
    print("\n✅ Aucune valeur manquante")