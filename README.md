# JTF One Piece TCG Analytics Project

A data engineering project that scrapes, processes, and analyzes One Piece Trading Card Game (OPTCG) tournament deck data using modern data stack tools.

## Overview

This project collects decklist data from OPTCG tournaments, transforms it using dbt, and provides analytics through a Tableau dashboard. It demonstrates end-to-end data pipeline orchestration with Dagster, supporting both local development (DuckDB) and cloud deployment (Google BigQuery).

## Features

- **Data Ingestion**: Automated scraping of decklists and leader card data from OPTCG websites
- **Data Transformation**: dbt models for staging, preparation, and mart layers
- **Orchestration**: Dagster pipelines for ETL workflows
- **Multi-Environment**: Local development with DuckDB, cloud deployment with BigQuery
- **Infrastructure as Code**: Terraform for GCP resource provisioning
- **Visualization**: Tableau dashboard for tournament analytics

## Tech Stack

- **Package Management**: uv
- **Orchestration**: Dagster
- **Transformation**: dbt
- **Databases**: DuckDB (local), Google BigQuery (cloud)
- **Scraping**: Python with BeautifulSoup4 and requests
- **IaC**: Terraform
- **Visualization**: Tableau
- **Language**: Python 3.13+

## Project Structure

```
├── jtf_optcg/              # dbt project
│   ├── models/
│   │   ├── raw/           # Source definitions
│   │   ├── stg/           # Staging models
│   │   ├── prep/          # Preparation models
│   │   └── mart/          # Mart models
│   ├── macros/            # Custom dbt macros
│   └── dbt_project.yml
├── orch/                   # Dagster orchestration
│   ├── assets/            # Dagster assets
│   ├── jobs/              # Dagster jobs
│   └── definitions.py     # Dagster definitions
├── setup/                  # Data ingestion scripts
│   ├── scrape_*.py        # Scraping scripts
│   ├── *_ingest.py        # Data loading scripts
│   └── terraform_infra.py # Infrastructure setup
├── pyproject.toml          # Python dependencies
└── README.md
```

## Setup Instructions

### Prerequisites

- Python 3.13+
- uv (Python package installer and resolver)
- Terraform

```
uv sync  # Installs dependencies and creates virtual environment
```
   > **Note**: This project uses uv for all Python package management. The `uv.lock` file ensures reproducible environments across all deployment scenarios.

**For cloud deployment only:**
- Google Cloud service account with appropriate permissions


### Local Development Setup

1. **Clone and install dependencies:**
   ```bash
   git clone <repository-url>
   cd jtf-project
   ```

2. **Set up DuckDB environment:**
   ```bash
   # Run the DuckDB ETL pipeline
   dagster job execute -f orch.definitions -j duck_extract_load
   ```

3. **Run dbt transformations:**
   ```bash
   # Run dbt models using Dagster
   dagster job execute -f orch.definitions -j duck_dbt_build_model
   ```

### Cloud Deployment Setup

1. **Create Google Cloud service account:**


2. **Update credentials file:**
   Place the downloaded `my_credentials.json` in the `setup/` directory.

3. **Run cloud pipeline:**
   ```bash
   dagster job execute -f orch.definitions -j gcp_infra
   dagster job execute -f orch.definitions -j gcp_bq_ingest
   dagster job execute -f orch.definitions -j gcp_dbt_build_model
   ```

## Usage

### Running the Pipeline

Start the Dagster webserver:
```bash
dagster dev
```
After running, you will see a message like
`- dagster-webserver - INFO - Serving dagster-webserver on`.

Access the UI at the shared URL to execute jobs manually or set up schedules.

### Data Scraping

Run individual scraping scripts:
```bash
python setup/scrape_decklists.py
python setup/scrape_leaders.py
```

### dbt Development

```bash
cd jtf_optcg
dbt compile          # Compile models
dbt test            # Run tests
dbt docs generate   # Generate documentation
dbt docs serve      # View documentation
```

## Data Model

- **Raw Layer**: Source data from scraped CSV files
- **Staging Layer**: Cleaned and standardized data
- **Preparation Layer**: Business logic transformations
- **Mart Layer**: Analytics-ready datasets for reporting

Key entities:
- Decklists: Tournament deck information
- Leaders: Leader card details with attributes

## Dashboard

View the Tableau dashboard: [OPTCG Analytics Dashboard](https://public.tableau.com/app/profile/jo.o.fernando1427/viz/optcg_dashboard/OPTCG)

## Development Notes

- Local development uses DuckDB for fast iteration
- Cloud deployment uses BigQuery for scalability
- GCP infrastructure (BigQuery datasets, storage buckets) is provisioned via Dagster's `gcp_infra` job
- Dagster orchestrates the entire ETL pipeline


## License

This project is for educational purposes as part of the Data Engineering Zoomcamp.