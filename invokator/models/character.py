"""TCG characters."""
import pydantic

from .effect import DiceCost, Effect
from .enums import Element, TalentType, WeaponType


class Talent(pydantic.BaseModel):
    """TCG character move."""

    id: int
    name: str
    type: TalentType
    cost: list[DiceCost]
    effects: list[Effect]


class Character(pydantic.BaseModel):
    """TCG character data."""

    id: int
    name: str
    energy: int
    health: int = 10
    element: Element
    weapon: WeaponType
    location: str

    talents: list[Talent]
    effects: list[Effect] = []
