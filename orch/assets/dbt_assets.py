from dagster import AssetExecutionContext, Config
from dagster_dbt import DbtCliResource, dbt_assets
from pathlib import Path

DBT_PROJECT_DIR = Path(__file__).parent.parent.parent / "jtf_optcg"

class DbtConfig(Config):
    target: str

@dbt_assets(
        manifest=DBT_PROJECT_DIR / "target" / "manifest.json",
        name="dbt_assets",
        )
def dbt_assets_fn(context: AssetExecutionContext, dbt: DbtCliResource, config: DbtConfig):
    yield from dbt.cli(["build", "--target", config.target], context=context).stream()

'''
@dbt_assets(
    manifest=DBT_PROJECT_DIR / "target" / "manifest.json",
    name="dbt_bigquery_assets",
    key_prefix="gcp"
)
def dbt_bigquery_assets(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build", "--target", "bigquery"], context=context).stream()

'''