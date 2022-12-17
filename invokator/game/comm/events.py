"""Event classes."""
import abc
import typing

import pydantic

from invokator import models
from invokator.game import enums

T = typing.TypeVar("T")

IntID = int
StrID = str

PlayerID = int


__all__ = ["BaseEvent", "DiscardEvent", "Event"]


class BaseEvent(typing.Generic[T], pydantic.BaseModel):
    """Base class for events."""


class Event(BaseEvent[None]):
    """Base class for game events without requiring any reply."""

    side: PlayerID
    """Which side this event is for."""


# ====================
# Turn events


class EndTurnEvent(Event):
    """The turn has been ended for a player."""


class StartTurnEvent(Event):
    """The turn has been started for a player."""


class EndPlayerRoundEvent(Event):
    """A player's round has ended."""


class EndRoundEvent(Event):
    """The round has ended for everyone."""

    side: typing.Literal[0] = 0
    """All sides."""


class StartRoundEvent(Event):
    """The round has started for everyone."""

    side: typing.Literal[0] = 0
    """All sides."""


# ====================
# Health events


class ChangeHealthEvent(Event, abc.ABC):
    """A character's health has changed."""

    target: IntID
    """The target of the health change."""

    current: int
    """The target's new current health."""

    @property
    @abc.abstractmethod
    def delta(self) -> int:
        """The health change."""


class HealEvent(ChangeHealthEvent):
    """A character has been healed."""

    heal: int
    """The heal amount."""

    @property
    def delta(self) -> int:
        return self.heal


class DamageEvent(ChangeHealthEvent):
    """A character has been damaged."""

    damage: int
    """The damage dealt."""

    @property
    def delta(self) -> int:
        return -self.damage


class TalentEvent(DamageEvent):
    """A character has used a talent."""

    source: IntID
    """The character that used this talent."""

    talent: IntID
    """The talent used."""


class SummonAttackEvent(DamageEvent):
    """A summon has attacked."""

    source: StrID
    """The summon that attacked."""


# ====================
# Element events


class ElementChangeEvent(Event):
    """A character's inflicted elements has changed."""

    target: IntID
    """The target of the element change."""

    current: list[models.Element]
    """The character's current inflicted elements."""


class ElementInflictEvent(ElementChangeEvent):
    """A character has been inflicted by an element."""

    target: IntID
    """The target of the element."""

    element: models.Element | None
    """The element inflicted."""


class ElementClearEvent(Event):
    """A character had their inflicted elements cleared."""

    current: list[models.Element] = []
    """The character's current inflicted elements."""


# ====================
# Summon events


class ChangeSummonEvent(Event):
    """A summon has been changed on the field."""

    summon: StrID
    """The summon that was changed."""


class CreateSummonEvent(ChangeSummonEvent):
    """A summon has been created on the field."""


class DecrementSummonEvent(ChangeSummonEvent):
    """A summon's duration has been decremented."""


class IncrementSummonEvent(ChangeSummonEvent):
    """A summon's duration has been incremented."""


class DestroySummonEvent(ChangeSummonEvent):
    """A summon has been destroyed."""


# ====================
# Support card events


class ChangeSupportEvent(Event):
    """A support card has been changed on the field."""

    card: IntID
    """The support card that was changed."""


class CreateSupportEvent(ChangeSupportEvent):
    """A support card has been created on the field."""


class DecrementSupportEvent(ChangeSupportEvent):
    """A support card's duration has been decremented."""


class IncrementSupportEvent(ChangeSupportEvent):
    """A support card's duration has been incremented."""


class DestroySupportEvent(ChangeSupportEvent):
    """A support card has been destroyed."""


# ====================
# Status events


class ChangeStatusEvent(Event):
    """A character's status has changed."""

    target: IntID
    """The character that had their status changed."""

    status: StrID
    """The status that was changed."""

    current: list[StrID]
    """The character's current statuses."""


class CreateStatusEvent(ChangeStatusEvent):
    """A character has been given a status."""


class RemoveStatusEvent(ChangeStatusEvent):
    """A character has had a status removed."""


class DecrementStatusEvent(ChangeStatusEvent):
    """A character's status duration has been decremented."""


class IncrementStatusEvent(ChangeStatusEvent):
    """A character's status duration has been incremented."""


# ====================
# Infusion events


class InfuseEvent(Event):
    """A character has been infused with an element."""

    target: IntID
    """The character that was infused."""

    element: models.Element
    """The element that was infused."""

    duration: int
    """The duration of the infusion."""


# ====================
# Switch events


class SwitchEvent(Event):
    """The active character has been switched."""

    target: IntID
    """The character that is now active."""

    previous: IntID
    """The previous character."""


# ====================
# Hand events


class HandChangeEvent(Event, abc.ABC):
    """The amount of cards in a hand has changed."""

    current: list[IntID] | None
    """The current cards in the hand.

    If this is None, the cards cannot be revealed.
    """

    @property
    @abc.abstractmethod
    def delta(self) -> int:
        """The change in cards."""


class DrawEvent(HandChangeEvent):
    """Cards have been drawn from the deck."""

    amount: int
    """The amount of cards drawn."""

    cards: list[IntID] | None
    """The cards that were drawn.

    If this is None, the cards cannot be revealed.
    """

    @property
    def delta(self) -> int:
        return self.amount


class DiscardEvent(HandChangeEvent):
    """Cards have been discarded from the hand."""

    amount: int
    """The amount of cards discarded."""

    cards: list[IntID] | None
    """The cards that were drawn.

    If this is None, the cards cannot be revealed.
    """

    @property
    def delta(self) -> int:
        return -self.amount


# ====================
# Dice events


class DiceChangeEvent(Event, abc.ABC):
    """Player's dice have changed."""

    current_amount: int
    """The current amount of dice."""

    current: list[models.Element] | None
    """The current dice.

    If this is None, the dice cannot be revealed.
    """

    @property
    @abc.abstractmethod
    def delta(self) -> int:
        """The change in dice."""


class DiceAddEvent(DiceChangeEvent):
    """Player's dice have changed."""

    amount: int
    """The amount of dice added."""

    dice: list[models.Element] | None
    """The dice that were added.

    If this is None, the dice cannot be revealed.
    """

    @property
    def delta(self) -> int:
        return self.amount


class DiceRemoveEvent(DiceChangeEvent):
    """Player's dice have changed."""

    amount: int
    """The amount of dice removed."""

    dice: list[models.Element] | None
    """The dice that were removed.

    If this is None, the dice cannot be revealed.
    """

    @property
    def delta(self) -> int:
        return -self.amount


class RequestEvent(BaseEvent[T]):
    """Base class for game events that require a reply."""


class ActionRequestEvent(RequestEvent[enums.Action]):
    """A player has been requested to take an action."""


class CardRequestEvent(RequestEvent[StrID]):
    """A player has been requested to choose a card."""

    possible: list[IntID]
    """The cards that can be chosen."""


class DiceRequestEvent(RequestEvent[list[models.Element]]):
    """A player has been requested to choose a dice."""

    cost: list[models.DiceCost]
    """The cost of the dice."""

    recommended: list[models.Element] | None
    """The recommended dice to choose."""


class TalentRequestEvent(RequestEvent[StrID]):
    """A player has been requested to choose a talent."""

    possible: list[IntID]
    """The talents that can be chosen."""


class CharacterRequestEvent(RequestEvent[IntID]):
    """A player has been requested to choose a character."""

    possible: list[IntID] | None
    """The characters that can be chosen."""

    possible_enemy: list[IntID] | None
    """The enemy characters that can be chosen."""


class SummonRequestEvent(RequestEvent[StrID]):
    """A player has been requested to choose a summon."""

    possible: list[IntID]
    """The summons that can be chosen."""

    possible_enemy: list[IntID] | None
    """The enemy summons that can be chosen."""


class SupportRequestEvent(RequestEvent[StrID]):
    """A player has been requested to choose a support card."""

    possible: list[IntID]
    """The support cards that can be chosen."""

    possible_enemy: list[IntID] | None
    """The enemy support cards that can be chosen."""
