# orchestration/definitions.py
from dagster import Definitions, load_assets_from_modules
from dagster_dbt import DbtCliResource
from pathlib import Path
from orch.assets import ingestion_assets, dbt_assets
from orch.jobs.jobs import duck_extract_load, duck_dbt_build_model, gcp_infra, gcp_bq_ingest, gcp_dbt_build_model

DBT_PROJECT_DIR = Path(__file__).parent.parent / "jtf_optcg"

all_assets = load_assets_from_modules([ingestion_assets, dbt_assets])

defs = Definitions(
    assets=all_assets,
    jobs=[duck_extract_load, duck_dbt_build_model, gcp_infra, gcp_bq_ingest, gcp_dbt_build_model],
    resources={
        "dbt": DbtCliResource(project_dir=str(DBT_PROJECT_DIR))
    }
)