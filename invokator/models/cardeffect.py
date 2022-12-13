"""TCG effect on cards."""
import pydantic

from .effect import Effect
from .enums import CardEffectAttachType


class CardEffect(pydantic.BaseModel):
    id: str
    usage: int
    invisible: bool = False
    attach: CardEffectAttachType = CardEffectAttachType.DYNAMIC
    effects: list[Effect]
