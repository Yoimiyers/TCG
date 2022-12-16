"""TCG effects."""
import typing

import pydantic
from typing_extensions import Self

from .enums import (
    CardDirection,
    EffectTriggerType,
    EffectType,
    Element,
    EquipmentType,
    ReactionType,
    SidelineLocation,
    SidelineTarget,
    TalentType,
)


class DiceCost(pydantic.BaseModel):
    """TCG dice cost."""

    amount: int = 0
    element: Element | None = None


class EffectTrigger(pydantic.BaseModel):
    """Effect trigger."""

    def __new__(cls, **kwargs: typing.Any) -> Self:
        """Dynamically create a subclass of EffectTrigger based on the type field."""
        return super().__new__(_TRIGGER_CLASSES.get(EffectTriggerType(kwargs["type"]), EffectTrigger))

    type: EffectTriggerType


class AttackTrigger(EffectTrigger):
    """Attack trigger."""

    type: EffectTriggerType = EffectTriggerType.ATTACK

    talent: TalentType | None = None
    reaction: ReactionType | None = None


class DamageTrigger(EffectTrigger):
    """Damage above trigger."""

    type: EffectTriggerType = EffectTriggerType.DAMAGE

    minimum: int | None = None
    maximum: int | None = None

    element: Element | None = None


_TRIGGER_CLASSES: dict[EffectTriggerType, type[EffectTrigger]] = {
    cls.__fields__["type"].default: cls
    for cls in EffectTrigger.__subclasses__()
    if "type" in cls.__fields__ and cls.__fields__["type"].default
}


class Effect(pydantic.BaseModel):
    """TCG attack effect."""

    def __new__(cls, **kwargs: typing.Any) -> Self:
        """Dynamically create a subclass of Effect based on the type field."""
        return super().__new__(_EFFECT_CLASSES.get(EffectType(kwargs["type"]), Effect))

    trigger: EffectTrigger | None = None

    type: EffectType


class CardEffect(Effect):
    """TCG card effect."""

    type: EffectType = EffectType.CARD

    id: str


class AttackEffect(Effect):
    """TCG attack effect."""

    type: EffectType = EffectType.ATTACK

    damage: int
    element: Element


class HealEffect(Effect):
    """TCG heal effect."""

    type: EffectType = EffectType.HEAL

    amount: int
    target: SidelineTarget = SidelineTarget.ACTIVE_CHARACTER


class SummonEffect(Effect):
    """TCG summon effect."""

    type: EffectType = EffectType.SUMMON

    id: str


class StatusEffect(Effect):
    """TCG status effect."""

    type: EffectType = EffectType.STATUS

    id: str
    target: SidelineTarget = SidelineTarget.ACTIVE_CHARACTER


class InfuseEffect(Effect):
    """TCG infuse effect."""

    type: EffectType = EffectType.INFUSE

    element: Element
    duration: int = 1


class SwitchEffect(Effect):
    """TCG switch effect."""

    type: EffectType = EffectType.SWITCH

    location: SidelineLocation
    direction: CardDirection = CardDirection.RIGHT


class BuffEffect(Effect):
    """TCG buff effect."""

    type: EffectType = EffectType.BUFF

    amount: int


class ClearEffect(Effect):
    """TCG clear effect."""

    type: EffectType = EffectType.CLEAR


class DiscountEffect(Effect):
    """TCG discount effect."""

    type: EffectType = EffectType.DISCOUNT

    dice: list[DiceCost]


class DecrementEffect(Effect):
    """TCG decrement effect."""

    type: EffectType = EffectType.DECREMENT

    amount: int = 1


class DrawEffect(Effect):
    """TCG draw effect."""

    type: EffectType = EffectType.DRAW

    amount: int


class AddDiceEffect(Effect):
    """TCG add dice effect."""

    type: EffectType = EffectType.ADDDICE

    dice: list[DiceCost]


class DestroyEffect(Effect):
    """TCG destroy effect."""

    type: EffectType = EffectType.DESTROY

    target: SidelineTarget
    location: SidelineLocation

    amount: int = 1


class ExtendEffect(Effect):
    """TCG extend effect."""

    type: EffectType = EffectType.EXTEND

    target: SidelineTarget
    location: SidelineLocation = SidelineLocation.FRIEND


class ShiftEffect(Effect):
    """TCG shift effect."""

    type: EffectType = EffectType.SHIFT

    slot: EquipmentType


class EnergyEffect(Effect):
    """TCG energy effect."""

    type: EffectType = EffectType.ENERGY

    amount: int
    target: SidelineTarget = SidelineTarget.ACTIVE_CHARACTER
    location: SidelineLocation = SidelineLocation.FRIEND


class ProtectEffect(Effect):
    """TCG protect effect."""

    type: EffectType = EffectType.PROTECT

    amount: int
    element: Element | None = None
    """To only protect against the specified element"""


class InstantEffect(Effect):
    """TCG instant effect."""

    type: EffectType = EffectType.QUICK


_EFFECT_CLASSES: dict[EffectType, type[Effect]] = {
    cls.__fields__["type"].default: cls
    for cls in Effect.__subclasses__()
    if "type" in cls.__fields__ and cls.__fields__["type"].default
}
