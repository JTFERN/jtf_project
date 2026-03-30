# setup/bigquery_ingest.py
from google.cloud import storage, bigquery
from pathlib import Path

CSV_DIR = Path(__file__).parent
CREDENTIALS = CSV_DIR / "my_credentials.json"  # path to your credentials file
PROJECT = "jtf-optcg"
BUCKET_NAME = "jtf2_optcg"
DATASET = "jtf_optcg"
LOCATION = "EU"

def upload_csv_to_gcs(filename: str) -> None:
    client = storage.Client.from_service_account_json(CREDENTIALS)
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob(filename)
    blob.upload_from_filename(CSV_DIR / filename)
    print(f"Uploaded {filename} to GCS")

def create_external_table(table_id: str, filename: str) -> None:
    client = bigquery.Client.from_service_account_json(CREDENTIALS, project=PROJECT)

    table_ref = f"{PROJECT}.{DATASET}.{table_id}"
    job_config = bigquery.ExternalConfig("CSV")
    job_config.source_uris = [f"gs://{BUCKET_NAME}/{filename}"]
    job_config.autodetect = True
    job_config.csv_options.skip_leading_rows = 1

    table = bigquery.Table(table_ref)
    table.external_data_configuration = job_config

    client.delete_table(table_ref, not_found_ok=True)
    client.create_table(table)
    print(f"External table {table_id} created")

def bigquery_ingest() -> None:
    upload_csv_to_gcs("decklists.csv")
    upload_csv_to_gcs("leaders.csv")
    create_external_table("decklists", "decklists.csv")
    create_external_table("leaders", "leaders.csv")
    print("BigQuery ingest complete")

if __name__ == "__main__":
    bigquery_ingest()