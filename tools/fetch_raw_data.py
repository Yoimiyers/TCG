import json
from typing import Any, Dict
from urllib import request
import re

API_URL = (
    "https://sg-hk4e-api-static.hoyoverse.com/event/e20221205drawcard/card_config?lang=zh-tw"
)


def fetch_cards() -> Dict[str, Any]:
    card_config = request.urlopen(API_URL).read()
    assert len(card_config) > 0

    data = json.loads(card_config.decode("utf-8"))["data"]
    assert data["role_card_infos"][0]["name"]

    # replace HTML tags
    pattern = re.compile(r"<.*?>")
    for card in data["role_card_infos"]:
        for skill in card["role_skill_infos"]:
            skill["skill_text"] = pattern.sub("", skill["skill_text"])
    for card in data["action_card_infos"]:
        card["content"] = pattern.sub("", card["content"])
    
    return data


if __name__ == "__main__":
    print("Fetching cards...")
    cards = fetch_cards()

    with open("raw_data/cards.json", "w") as f:
        json.dump(cards, f, indent=2, ensure_ascii=False)

    print("Done.")