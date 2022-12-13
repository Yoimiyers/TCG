"""TCG characters."""
import pydantic

from .effect import DiceCost, Effect
from .enums import Element, TalentType


class Talent(pydantic.BaseModel):
    """TCG character move."""

    type: TalentType
    cost: list[DiceCost]
    effects: list[Effect]


class Character(pydantic.BaseModel):
    """TCG character data."""

    name: str
    energy: int
    element: Element
    weapon: str
    location: str

    talents: list[Talent]
