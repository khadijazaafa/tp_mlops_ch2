import dlt
import pandas as pd

# Définir la ressource dlt
@dlt.resource(name="csv_data", write_disposition="replace")
def csv_data():
    df = pd.read_csv("data/source.csv")
    
    # Nettoyer les valeurs manquantes avant ingestion
    df["montant"] = df["montant"].fillna(0.0)
    
    yield df.to_dict(orient="records")

# Créer le pipeline dlt vers DuckDB
pipeline = dlt.pipeline(
    pipeline_name="tp_pipeline",
    destination="duckdb",
    dataset_name="raw"
)

# Lancer l'ingestion
print("=== Lancement de l'ingestion ===")
load_info = pipeline.run(csv_data())
print(load_info)

# Vérification : lire les données depuis DuckDB
import duckdb

print("\n=== Vérification dans DuckDB ===")
conn = duckdb.connect("tp_pipeline.duckdb")
result = conn.execute("SELECT * FROM raw.csv_data").fetchdf()
print(result)
print(f"\n✅ {len(result)} lignes chargées dans DuckDB")
conn.close()