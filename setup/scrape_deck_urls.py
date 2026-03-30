"""
Extracts all decklist URLs from https://onepiecetopdecks.com/deck-list/
The page uses Elementor image widgets where each image is wrapped in an <a> tag
pointing to an individual deck list page.
Requirements:
    pip install requests beautifulsoup4 pandas
Usage:
    python scrape_deck_urls.py
    --> outputs deck_urls.csv and prints a DataFrame
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd
from pathlib import Path

CSV_DIR = Path(__file__).parent  # same folder

URL = "https://onepiecetopdecks.com/deck-list/"

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

def extract_deck_urls(soup: BeautifulSoup) -> pd.DataFrame:
    base = "https://onepiecetopdecks.com/deck-list/"
    seen = set()
    records = []

    for widget in soup.select("div.elementor-widget-image"):
        a = widget.find("a", href=True)
        if not a:
            continue
        href = a["href"].strip()
        if not href.startswith(base) or href == base:
            continue
        if href in seen:
            continue
        seen.add(href)
        records.append({"url": href})

    df = pd.DataFrame(records, columns=["url"])
    df["is_english"] = df["url"].str.contains("deck-list/en-format-|deck-list/english-", regex=True).astype(int)
    df = df.loc[df["is_english"] > 0, ["url"]].reset_index(drop=True)
    df["set_name"] = df["url"].str.rstrip("/").str.extract(r"deck-list/(?:en-format-|english-)(.+)$")

    return df

def get_deck_urls() -> pd.DataFrame:
    soup = fetch(URL)
    return extract_deck_urls(soup)

def save_deck_urls() -> None:
    df = get_deck_urls()
    df.to_csv(CSV_DIR / "deck_urls.csv", index=False)
    print(f"Fetched: {len(df)} sets")

if __name__ == "__main__":
    save_deck_urls()
    #print(df)

