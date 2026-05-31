import sys
import dlt
import pandas as pd
import duckdb

sys.stdout.reconfigure(encoding='utf-8')

@dlt.resource(name="csv_data", write_disposition="replace")
def csv_data():
    df = pd.read_csv("data/source.csv")
    df["montant"] = df["montant"].fillna(0.0)
    yield df.to_dict(orient="records")

pipeline = dlt.pipeline(
    pipeline_name="tp_pipeline",
    destination="duckdb",
    dataset_name="raw"
)

print("=== Lancement de l'ingestion ===")
load_info = pipeline.run(csv_data())
print(load_info)

print("\n=== Verification dans DuckDB ===")
conn = duckdb.connect("tp_pipeline.duckdb")
result = conn.execute("SELECT * FROM raw.csv_data").fetchdf()
print(result)
print(f"\nOK : {len(result)} lignes chargees dans DuckDB")
conn.close()