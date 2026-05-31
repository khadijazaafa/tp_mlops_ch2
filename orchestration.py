import subprocess
import sys
from pathlib import Path
from dagster import op, job, Out, In

# Chemins
PYTHON       = sys.executable
DBT          = str(Path(sys.executable).parent / "dbt.exe")
PROFILES_DIR = str(Path.home() / ".dbt")
PROJECT_DIR  = "tp_dbt"

@op(out=Out(bool))
def op_charger_csv(context):
    context.log.info("Chargement et validation du CSV...")
    result = subprocess.run(
        [PYTHON, "load_csv.py"],
        capture_output=True, text=True, encoding="utf-8"
    )
    context.log.info(result.stdout)
    if result.returncode != 0:
        raise Exception(f"Erreur load_csv:\n{result.stderr}")
    return True

@op(ins={"precedent": In(bool)}, out=Out(bool))
def op_ingestion(context, precedent):
    context.log.info("Ingestion avec dlt...")
    result = subprocess.run(
        [PYTHON, "ingest.py"],
        capture_output=True, text=True, encoding="utf-8"
    )
    context.log.info(result.stdout)
    if result.returncode != 0:
        raise Exception(f"Erreur ingest:\n{result.stderr}")
    return True

@op(ins={"precedent": In(bool)}, out=Out(bool))
def op_transformation(context, precedent):
    context.log.info("Transformation avec dbt run...")
    result = subprocess.run(
        [DBT, "run",
         "--project-dir", PROJECT_DIR,
         "--profiles-dir", PROFILES_DIR],
        capture_output=True, text=True, encoding="utf-8"
    )
    context.log.info(result.stdout)
    if result.returncode != 0:
        raise Exception(f"Erreur dbt run:\n{result.stderr}")
    return True

@op(ins={"precedent": In(bool)})
def op_tests_qualite(context, precedent):
    context.log.info("Tests qualite avec dbt test...")
    result = subprocess.run(
        [DBT, "test",
         "--project-dir", PROJECT_DIR,
         "--profiles-dir", PROFILES_DIR],
        capture_output=True, text=True, encoding="utf-8"
    )
    context.log.info(result.stdout)
    if result.returncode != 0:
        raise Exception(f"Erreur dbt test:\n{result.stderr}")
    context.log.info("Pipeline termine avec succes !")

@job
def pipeline_mlops():
    op_tests_qualite(
        op_transformation(
            op_ingestion(
                op_charger_csv()
            )
        )
    )