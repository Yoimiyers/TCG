"""Test stored carddata."""
import json
import os
import typing

import pydantic

import invokator


def _dump_card_data(data: typing.Sequence[pydantic.BaseModel], file: str) -> None:
    """Dump card data to a temporary JSON file."""
    os.makedirs(".temporary/carddata", exist_ok=True)
    file = ".temporary/carddata/" + file

    decoded = [json.loads(x.json()) for x in data]
    decoded.sort(key=lambda x: x["id"])

    json.dump(decoded, open(file, "w", encoding="utf-8"), indent=4)


def test_carddata() -> None:
    """Validate stored carddata."""
    assert all(isinstance(x, invokator.models.Card) for x in invokator.models.CARDS)
    assert all(isinstance(x, invokator.models.Character) for x in invokator.models.CHARACTERS)
    assert all(isinstance(x, invokator.models.CardStatus) for x in invokator.models.EFFECTS)
    assert all(isinstance(x, invokator.models.Summon) for x in invokator.models.SUMMONS)

    # finish by dumping the card data to temporary files
    _dump_card_data(invokator.models.CARDS, "cards.json")
    _dump_card_data(invokator.models.CHARACTERS, "characters.json")
    _dump_card_data(invokator.models.EFFECTS, "status.json")
    _dump_card_data(invokator.models.SUMMONS, "summons.json")
