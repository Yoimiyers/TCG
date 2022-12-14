"""Player interface."""
from invokator import models

from .character import Character
from .deck import Deck
from .dice import Dice
from .hand import Hand
from .summon import Summon

__all__ = ["Player"]


class Player:
    """Player interface."""

    characters: list[Character]
    deck: Deck

    active_character: Character | None  # pointer

    hand: Hand
    dice: Dice

    summons: list[Summon]

    def __init__(
        self,
        characters: list[Character],
        deck: list[models.Card],
    ) -> None:
        self.characters = characters
        self.deck = Deck(deck)

        self.active_character = None

        self.hand = Hand()
        self.dice = Dice(preferred_elements=self._usable_elements)

        self.summons = []

    @property
    def alive_characters(self) -> list[Character]:
        """Return list of alive characters."""
        return [character for character in self.characters if character.current_health > 0]

    @property
    def _usable_elements(self) -> list[models.Element]:
        """Return list of usable elements."""
        return [character.element for character in self.alive_characters]

    def switch_character(self, index: int) -> None:
        """Switch active character."""
        self.active_character = self.characters[index]
        self.dice.preferred_elements = [
            self.characters[index].element,
            *self._usable_elements,
        ]

    def clear_expired_effects(self) -> None:
        """Clear all effects that have ran out."""
        for character in self.characters:
            character.effects = [effect for effect in character.effects if effect.duration > 0]

        self.summons = [summon for summon in self.summons if summon.usage_left > 0]
