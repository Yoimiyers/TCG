"""TCG effects."""
import typing

import pydantic
from typing_extensions import Self

from .enums import (CardPosition, EffectTrigger, EffectType, Element, EquipmentType,
                    SidelineTarget, TalentType)


class DiceCost(pydantic.BaseModel):
    """TCG dice cost."""

    amount: int = 0
    element: Element | None = None
    same_element: bool = False # require all dice to be the same element


class Effect(pydantic.BaseModel):
    """TCG card effect."""

    def __new__(cls, **kwargs: typing.Any) -> Self:
        return super().__new__(_EFFECT_CLASSES[EffectType(kwargs["type"])])

    trigger: EffectTrigger = EffectTrigger.USED
    type: EffectType


class DamageEffect(Effect):
    """TCG damage effect."""

    type: EffectType = EffectType.DAMAGE

    amount: int
    element: Element


class HealEffect(Effect):
    """TCG heal effect."""

    type: EffectType = EffectType.HEAL

    amount: int


class SummonEffect(Effect):
    """TCG summon effect."""

    type: EffectType = EffectType.SUMMON

    id: str # the card id to summon


class CustomEffect(Effect):
    """TCG custom effect."""

    type: EffectType = EffectType.CUSTOM

    id: str


class InfuseEffect(Effect):
    """TCG element infusion effect."""

    type: EffectType = EffectType.INFUSE

    element: Element


class SwitchEffect(Effect):
    """TCG switch effect."""

    type: EffectType = EffectType.SWITCH

    instant: bool = False


class ForceSwitchEffect(Effect):
    """TCG force switch effect."""

    type: EffectType = EffectType.FORCESWITCH
    
    position: CardPosition


class BuffEffect(Effect):
    """TCG damage buff effect."""

    type: EffectType = EffectType.BUFF

    talent: TalentType
    amount: int


class ClearEffect(Effect):
    """TCG clear effect."""

    type: EffectType = EffectType.CLEAR


class DiscountEffect(Effect):
    """TCG dice discount effect."""

    type: EffectType = EffectType.DISCOUNT

    dice: list[DiceCost]


class DecrementEffect(Effect):
    """TCG decrement effect."""

    type: EffectType = EffectType.DECREMENT

    amount: int = 1


class DrawEffect(Effect):
    """TCG draw card effect."""

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


class ExtendEffect(Effect):
    """TCG extend effect."""

    type: EffectType = EffectType.EXTEND

    target: SidelineTarget


class SwapEffect(Effect):
    """TCG swap equipment effect."""

    type: EffectType = EffectType.SWAP

    slot: EquipmentType


class EnergyEffect(Effect):
    """TCG character gain energy effect."""

    type: EffectType = EffectType.ENERGY

    amount: int
    target: SidelineTarget = SidelineTarget.ACTIVE_CHARACTER
    
class DiceReduceEffect(Effect):
    """TCG dice reduce effect."""
    
    type: EffectType = EffectType.DICEREDUCE
    
    amount: int
    talent: TalentType
    element: typing.Optional[Element] = None

class ProtectEffect(Effect):
    """TCG protect effect."""

    type: EffectType = EffectType.PROTECT

    amount: int # amount of damage to protect against
    element: typing.Optional[Element] = None
    trigger: EffectTrigger

_EFFECT_CLASSES: dict[EffectType, type[Effect]] = {
    cls.__fields__["type"].default: cls
    for cls in Effect.__subclasses__()
    if "type" in cls.__fields__ and cls.__fields__["type"].default
}
