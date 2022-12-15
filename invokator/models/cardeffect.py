"""TCG effect on cards."""
import pydantic

from .effect import Effect
from .enums import CardStatusAttachType


class CardStatus(pydantic.BaseModel):
    """Status attached to a card."""

    id: str
    usage: int
    invisible: bool = False
    attach: CardStatusAttachType = CardStatusAttachType.DYNAMIC
    effects: list[Effect]
