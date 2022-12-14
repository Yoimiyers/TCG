"""Tools to fetch data and convert to a good format."""
import json
import re
import typing
import urllib.request

BASE_URL = "https://sg-hk4e-api-static.hoyoverse.com/event/e20221205drawcard/card_config?lang="

__all__ = ["fetch_cards"]


def fetch_cards() -> typing.Dict[str, typing.Any]:
    """Fetch card raw data in Traditional Chinese and remove HTML tags."""
    r = urllib.request.urlopen(BASE_URL + "zh-tw")
    card_config = r.read()
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
