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

    def remove_card(self, id: int) -> models.Card:
        """Remove a card from the hand."""
        for index, card in enumerate(self.cards):
            if card.id == id:
                return self.cards.pop(index)

        raise ValueError(f"Card with id {id} not found in hand.")

    def __getitem__(self, index: int) -> models.Card:
        """Get a card from the hand."""
        return self.cards[index]

    @property
    def amount(self) -> int:
        """Return the amount of cards in the hand."""
        return len(self.cards)

    @property
    def card_ids(self) -> list[int]:
        """Return the ids of the cards in the hand."""
        return [card.id for card in self.cards]
