"""Playground experimentation."""
import json
import typing

import pydantic

import invokator

T = typing.TypeVar("T")


def load_card_data(file: str, *, cls: type[T]) -> list[T]:
    """Load card data from a JSON file."""
    file = "carddata/" + file
    data = json.load(open(file, encoding="utf-8"))
    return pydantic.parse_obj_as(typing.List[cls], data)


cards = load_card_data("cards.json", cls=invokator.models.Card)
characters = load_card_data("characters.json", cls=invokator.interface.Character)
effects = load_card_data("effects.json", cls=invokator.models.CardEffect)
summons = load_card_data("summons.json", cls=invokator.models.Summon)

player = invokator.interface.Player(characters[:3], deck=cards)
print(player)
