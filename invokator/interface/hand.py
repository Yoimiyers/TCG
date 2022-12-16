"""Hand interface."""
from invokator import models

__all__ = ["Hand"]

CARD_TYPE_ORDER = (
    models.CardType.CHARACTER,
    models.CardType.EVENT,
    models.CardType.SUPPORT,
    models.CardType.WEAPON,
    models.CardType.ARTIFACT,
)


class Hand:
    """TCG hand interface."""

    cards: list[models.Card]

    def __init__(self, cards: list[models.Card] | None = None) -> None:
        self.cards = cards or []
        self._sort_cards()

    def _sort_cards(self) -> None:
        """Sort the cards by type."""
        self.cards.sort(key=lambda card: (CARD_TYPE_ORDER.index(card.type), card.name))

    def add_cards(self, cards: list[models.Card]) -> None:
        """Shuffle the hand."""
        self.cards.extend(cards)
        self._sort_cards()

    def remove_cards(self, index: int) -> None:
        """Remove a card from the hand."""
        self.cards.pop(index)

    def __getitem__(self, index: int) -> models.Card:
        """Get a card from the hand."""
        return self.cards[index]
