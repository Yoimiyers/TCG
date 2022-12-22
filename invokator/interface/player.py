"""Player interface."""
import typing

from invokator import models

from .character import Character
from .deck import Deck
from .dice import Dice
from .hand import Hand
from .summon import Summon

__all__ = ["Player"]


class Player:
    """Player interface."""

    id: int
    characters: list[Character]
    deck: Deck

    active_character: Character | None  # pointer

    hand: Hand
    dice: Dice

    summons: list[Summon]

    declared_end: bool

    def __init__(
        self,
        id: int,
        characters: list[Character],
        deck: list[models.Card],
    ) -> None:
        self.id = id
        self.characters = characters
        self.deck = Deck(deck)

        self.active_character = None

        self.hand = Hand()
        self.dice = Dice(preferred_elements=self._usable_elements)

        self.summons = []

        self.declared_end = False

    @property
    def alive_characters(self) -> list[Character]:
        """Return list of alive characters."""
        return [character for character in self.characters if character.current_health > 0]

    @property
    def _usable_elements(self) -> list[models.Element]:
        """Return list of usable elements."""
        return [character.element for character in self.alive_characters]

    def switch_character(self, id: int) -> None:
        """Switch active character."""
        character = next((character for character in self.characters if character.id == id), None)
        if character is None:
            raise ValueError("Invalid character id.")

        self.active_character = character
        self.dice.preferred_elements = [
            character.element,
            *self._usable_elements,
        ]

    def clear_expired_effects(self) -> None:
        """Clear all effects that have ran out."""
        for character in self.characters:
            character.status = [effect for effect in character.status if effect.duration > 0]

        self.summons = [summon for summon in self.summons if summon.usage_left > 0]

    def draw_cards(self, amount: int) -> list[models.Card]:
        """Draw cards from deck."""
        cards = self.deck.draw_multiple(amount)
        self.hand.add_cards(cards)
        return cards

    def dict(self) -> dict[str, typing.Any]:
        """Return dict representation of player."""
        return {
            "id": self.id,
            "characters": [character.dict() for character in self.characters],
            "active_character": self.active_character and self.active_character.id,
            "deck": self.deck.amount,
            "hand": [card.dict() for card in self.hand.cards],
            "dice": [die.value for die in self.dice.dice],
            "summons": [summon.dict() for summon in self.summons],
            "declared_end": self.declared_end,
        }
