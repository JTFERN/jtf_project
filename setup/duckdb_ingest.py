import duckdb
from pathlib import Path

CSV_DIR = Path(__file__).parent  # same folder as duckdb_ingest.py

def duck_create():
    con = duckdb.connect(str(CSV_DIR / "op.duckdb"))
    con.execute("CREATE SCHEMA IF NOT EXISTS dev")

    con.execute(f"""
        CREATE OR REPLACE TABLE dev.leaders AS
        SELECT * FROM read_csv_auto('{CSV_DIR / "leaders.csv"}')
    """)

    con.execute(f"""
        CREATE OR REPLACE TABLE dev.decklists AS
        SELECT * FROM read_csv_auto('{CSV_DIR / "decklists.csv"}')
    """)

    con.close()
    print("Tables loaded to DuckDB")

if __name__ == "__main__":
    duck_create()