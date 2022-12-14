"""TCG card data."""
import typing

import pydantic
from typing_extensions import Self

from .effect import DiceCost, Effect
from .enums import CardType, EquipmentType


class Card(pydantic.BaseModel):
    """TCG card data."""

    def __new__(cls, **kwargs: typing.Any) -> Self:
        return super().__new__(_CARD_CLASSES[CardType(kwargs["type"])])

    type: CardType
    name: str
    cost: DiceCost


class EquipmentCard(Card):
    """TCG equipment card data."""

    type: CardType = CardType.EQUIPMENT

    slot: EquipmentType
    effects: list[Effect]


class EventCard(Card):
    """TCG event card data."""

    type: CardType = CardType.EVENT

    effects: list[Effect]

class FoodCard(Card):
    """TCG food card data."""

    type: CardType = CardType.FOOD

    effects: list[Effect]

_CARD_CLASSES: dict[CardType, type[Card]] = {
    cls.__fields__["type"].default: cls
    for cls in Card.__subclasses__()
    if "type" in cls.__fields__ and cls.__fields__["type"].default
}
