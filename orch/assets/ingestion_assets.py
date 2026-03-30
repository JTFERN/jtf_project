from dagster import asset
from setup.scrape_leaders import get_leaders 
from setup.scrape_deck_urls import save_deck_urls 
from setup.scrape_decklists import get_decklist 
from setup.duckdb_ingest import duck_create
from setup.terraform_infra import provision_infra
from setup.bigquery_ingest import bigquery_ingest  


@asset(group_name="extract")
def leaders():
    return get_leaders()

@asset(group_name="extract")
def deck_urls():
    return save_deck_urls()

@asset(group_name="extract")
def decklist():
    return get_decklist()

@asset(group_name="duck", deps=[leaders, deck_urls, decklist])
def duck_ingest():
    return duck_create()

@asset(group_name="gcp")
def gcp_terraform():
    return provision_infra()

@asset(group_name="gcp", deps=[leaders, deck_urls, decklist, gcp_terraform])
def gcp_bq_ingest():
    return bigquery_ingest()