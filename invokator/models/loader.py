"""Load models from a directory."""

import pathlib
import typing
import warnings

import pydantic

from . import card, character, status, summon

__all__ = ["CARDS", "CHARACTERS", "EFFECTS", "SUMMONS"]

T = typing.TypeVar("T")

# ./invokator/models/loader.py -> ./carddata
top: pathlib.Path = (pathlib.Path(__file__) / ".." / ".." / "..").resolve()
DIRECTORY = top / "carddata"


def load_card_data(file: str | pathlib.Path, *, cls: type[T]) -> list[T]:
    """Load card data from a JSON file."""
    try:
        return pydantic.tools.parse_file_as(typing.List[cls], DIRECTORY / file)
    except Exception as e:
        warnings.warn("Failed to load card data.", source=e)
        return []


SUMMONS = load_card_data("summons.json", cls=summon.Summon)
CARDS = load_card_data("cards.json", cls=card.Card)
CHARACTERS = load_card_data("characters.json", cls=character.Character)
EFFECTS = load_card_data("status.json", cls=status.CardStatus)
