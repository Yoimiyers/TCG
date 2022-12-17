"""Fetch raw card data."""
import json
import os

from .raw import fetch_cards

if __name__ == "__main__":
    print("Fetching cards...")  # noqa: T201
    cards = fetch_cards()

    os.makedirs("carddata/raw", exist_ok=True)

    with open("carddata/raw/cards.json", "w", encoding="utf-8") as f:
        json.dump(cards, f, indent=4, ensure_ascii=False)

    print("Done.")  # noqa: T201
