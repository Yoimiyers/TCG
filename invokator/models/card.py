"""TCG card data."""
import typing

import pydantic
from typing_extensions import Self

from .effect import DiceCost, Effect
from .enums import CardType, Element, WeaponType


class Card(pydantic.BaseModel):
    """TCG card data."""

    def __new__(cls, **kwargs: typing.Any) -> Self:
        """Dynamically create a subclass of Card based on the type field."""
        return super().__new__(_CARD_CLASSES[CardType(kwargs["type"])])

    type: CardType

    id: int
    name: str
    cost: DiceCost


class WeaponCard(Card):
    """TCG equipment card data."""

    type: CardType = CardType.WEAPON

    weapon: WeaponType

    effects: list[Effect]


class ArtifactCard(Card):

    type: CardType = CardType.ARTIFACT

    element: Element | None = None

    effects: list[Effect]


class EventCard(Card):
    """TCG event card data."""

    type: CardType = CardType.EVENT

    effects: list[Effect]


_CARD_CLASSES: dict[CardType, type[Card]] = {
    cls.__fields__["type"].default: cls
    for cls in Card.__subclasses__()
    if "type" in cls.__fields__ and cls.__fields__["type"].default
}
