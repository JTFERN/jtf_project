# orch/jobs/jobs.py
from dagster import define_asset_job, AssetSelection
from orch.assets.dbt_assets import dbt_assets_fn
from dagster_dbt import build_dbt_asset_selection

duck_extract_load = define_asset_job(
    name="duck_db_01_extract_load",
    selection=AssetSelection.groups("extract") | AssetSelection.assets("duck_ingest")
)

duck_dbt_build_model = define_asset_job(
    name="duck_db_02_dbt_build",
    selection=build_dbt_asset_selection([dbt_assets_fn]),
    config={
        "ops": {
            "dbt_assets": {
                "config": {"target": "duckdb"}
            }
        }
    },
)

'''
duck_full_job = define_asset_job(
    name="duck_db_full_pipeline",
    selection=(
        AssetSelection.groups("extract")
        | AssetSelection.assets("duck_ingest")
        | build_dbt_asset_selection([dbt_duckdb_assets])
    )
)

'''

gcp_infra = define_asset_job(
    name="gcp_01_infra_start",
    selection= AssetSelection.assets("gcp_terraform")
)

gcp_bq_ingest = define_asset_job(
    name="gcp_02_bq_extract_load",
    selection= AssetSelection.groups("extract") | AssetSelection.assets("gcp_bq_ingest")
)

gcp_dbt_build_model = define_asset_job(
    name="gcp_03_dbt_build",
    selection=build_dbt_asset_selection([dbt_assets_fn]),
    config={
        "ops": {
            "dbt_assets": {
                "config": {"target": "bigquery"}
            }
        }
    },
)