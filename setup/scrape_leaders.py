"""
Scraper for One Piece Limitless TCG - All Leader Cards
URL: https://onepiece.limitlesstcg.com/cards/?q=category%3Aleader+sort%3Acolor+unique%3Acards&display=compact&show=all

Page structure (from inspection):
  Each card is a div.card-classic containing:
    - div.image > img           (image URL)
    - div.card-text-title       (name + card ID)
    - p.card-text-type          (category • color • life)
    - p.card-text-section       (power • attribute)
    - div.card-text-section[1]  (card effect text)
    - div.card-text-section[2]  (card type/affiliation, has data-tooltip="Type")

Requirements:
    pip install requests beautifulsoup4 pandas

Usage:
    python scrape_leaders.py
    --> returns DataFrame, outputs leaders.csv
"""

import re
import requests
from bs4 import BeautifulSoup
import pandas as pd
from pathlib import Path

CSV_DIR = Path(__file__).parent  # same folder

URL = (
    "https://onepiece.limitlesstcg.com/cards/"
    "?q=category%3Aleader+sort%3Acolor+unique%3Acards&display=compact&show=all"
)

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


def parse_card(card_div) -> dict:

    # --- Name and Card ID (e.g. "Edward.Newgate OP02-001") ---
    title_el = card_div.select_one("p.card-text-title")
    title_text = title_el.get_text(strip=True) if title_el else ""
    # Split on last whitespace-separated token that looks like a card ID
    id_match = re.search(r"^(.+?)\s+([A-Z0-9]+-\d+|P-\d+|ST\d+-\d+)$", title_text)
    name    = id_match.group(1) if id_match else title_text
    #card_id = id_match.group(2) if id_match else ""

    # --- Type line: "Leader • Red • 6 Life" ---
    type_el = card_div.select_one("p.card-text-type")
    type_text = type_el.get_text(strip=True) if type_el else ""
    # Split on bullet character
    type_parts = [p.strip() for p in type_text.split("•")]
    color    = type_parts[1] if len(type_parts) > 1 else ""
    life     = re.sub(r"\D", "", type_parts[2]) if len(type_parts) > 2 else ""

    # --- Power and Attribute: "6000 Power • Special" ---
    power_el = card_div.select_one("p.card-text-section")
    power_text = power_el.get_text(strip=True) if power_el else ""
    power_match = re.search(r"([\d,]+)\s+Power", power_text)
    power = power_match.group(1).replace(",", "") if power_match else ""


    return {
        "name":        name,
        "color":       color,
        "life":        life,
        "power":       power
    }


def get_leaders() -> pd.DataFrame:
    soup = fetch(URL)
    cards = soup.select("div.card-classic")
    records = [parse_card(c) for c in cards]
    df = pd.DataFrame(records)
    df.to_csv(CSV_DIR / "leaders.csv", index=False)
    print(f"Extracted {len(df)} leaders.")
    return 


if __name__ == "__main__":
    get_leaders()
    #print(df)