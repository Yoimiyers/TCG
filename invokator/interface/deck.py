"""Deck interface."""
import random

from invokator import models

__all__ = ["Deck"]


class Deck:
    """TCG deck interface."""

    cards: list[models.Card]

    def __init__(self, cards: list[models.Card]) -> None:
        self.cards = cards
        self.shuffle()

    def shuffle(self) -> None:
        """Shuffle the deck."""
        random.shuffle(self.cards)

    def draw(self) -> models.Card:
        """Draw a card from the deck."""
        return self.cards.pop()

    def draw_multiple(self, amount: int = 5) -> list[models.Card]:
        """Preview the top card of the deck."""
        return [self.cards.pop() for _ in range(min(amount, self.amount))]

    def reshuffle(self, cards: list[models.Card]) -> list[models.Card]:
        """Return cards back to deck and draw a new hand."""
        self.cards.extend(cards)
        self.shuffle()
        return self.draw_multiple(len(cards))

    @property
    def amount(self) -> int:
        """Return the amount of cards in the deck."""
        return len(self.cards)

    @property
    def card_ids(self) -> list[int]:
        """Return list of card ids."""
        return [card.id for card in self.cards]
