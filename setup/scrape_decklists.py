"""
Scraper for One Piece Top Decks - All English Deck Lists
Fetches all English deck URLs using scrape_deck_urls.get_deck_urls(),
then scrapes each deck's TablePress table and combines into a single DataFrame.

Requirements:
    pip install requests beautifulsoup4 pandas
Usage:
    python scrape_onepiece_decklist.py
    --> outputs decklist-<date>.json and prints a DataFrame
"""
import datetime
import time
import requests
from bs4 import BeautifulSoup
import pandas as pd
from pathlib import Path

CSV_DIR = Path(__file__).parent  # same folder

from setup.scrape_deck_urls import get_deck_urls

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    )
}

def fetch(url: str) -> BeautifulSoup:
    response = requests.get(url, headers=HEADERS, timeout=15)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")

def extract(soup: BeautifulSoup, url: str) -> dict:
    h1 = soup.find("h1")
    title = h1.get_text(strip=True) if h1 else ""

    shortcode_widget = soup.select_one("div.elementor-widget-shortcode")
    tables = []
    if shortcode_widget:
        for table in shortcode_widget.find_all("table"):
            headers = []
            thead = table.find("thead")
            if thead:
                headers = [th.get_text(strip=True) for th in thead.find_all(["th", "td"])]
            rows = []
            tbody = table.find("tbody")
            if tbody:
                for tr in tbody.find_all("tr"):
                    cells = [td.get_text(strip=True) for td in tr.find_all(["td", "th"])]
                    row = dict(zip(headers, cells)) if headers else cells
                    rows.append(row)
            tables.append({
                "table_id": table.get("id", ""),
                "headers": headers,
                "rows": rows,
            })

    return {"title": title, "url": url, "tables": tables}

def get_decklist() -> pd.DataFrame:
    urls_df = get_deck_urls()
    all_data = []
    all_dfs = []

    print(f"Found {len(urls_df)} English deck URLs to scrape.\n")

    for _, row in urls_df.iterrows():
        url = row["url"]
        set_name = row["set_name"]
        

        try:
            soup = fetch(url)
            data = extract(soup, url)
            all_data.append(data)

            for table in data["tables"]:
                if table["rows"]:
                    df = pd.DataFrame(table["rows"])
                    df["leader_id"] = df["Deck Composition"].str.extract(r"\dn(.+?)a")
                    df["table_id"] = table["table_id"]
                    df["set_name"] = set_name
                    df["source_url"] = url
                    all_dfs.append(df)
                    print(f"Fetching: {set_name} - {len(df)} entries")

        except Exception as e:
            print(f"  ERROR scraping {url}: {e}")

        time.sleep(0.5)  # be polite

    date = datetime.date.today()
    '''
    filename = f"decklist-{date}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(all_data, f, indent=2, ensure_ascii=False)
    print(f"\nSaved {len(all_data)} deck(s) to {filename}")
    '''
    
    df = pd.concat(all_dfs, ignore_index=True) if all_dfs else pd.DataFrame()
    print(f"Fetched: {len(df)} total entries")
    
    df=df.iloc[:,[3,4,5,6,7,8,9,10,11,13]] #filtering the df
    df["extraction_dt"]=date #adding extraction date
    df.to_csv(CSV_DIR / "decklists.csv", index=False)
    

if __name__ == "__main__":
    get_decklist()