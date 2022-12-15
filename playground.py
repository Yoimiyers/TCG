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


def decode_card_data(**kwargs: list[typing.Any]) -> dict[str, list[dict[str, typing.Any]]]:
    """Turn card data back into json."""
    return {key: [json.loads(x.json()) for x in data] for key, data in kwargs.items()}


cards = load_card_data("cards.json", cls=invokator.models.Card)
characters = load_card_data("characters.json", cls=invokator.interface.Character)
effects = load_card_data("status.json", cls=invokator.models.CardStatus)
summons = load_card_data("summons.json", cls=invokator.models.Summon)

player = invokator.interface.Player(characters[:3], deck=cards)
print(player)
