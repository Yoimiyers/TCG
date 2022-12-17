"""Dice interface."""
import random

from invokator import models

__all__ = ["Dice"]

ELEMENTS = [
    models.Element.ANEMO,
    models.Element.CRYO,
    models.Element.DENDRO,
    models.Element.ELECTRO,
    models.Element.GEO,
    models.Element.HYDRO,
    models.Element.PYRO,
    models.Element.OMNI,
]


class Dice:
    """Dice interface."""

    dice: list[models.Element]
    preferred_elements: list[models.Element]

    def __init__(self, *, preferred_elements: list[models.Element]) -> None:
        self.dice = []
        self.preferred_elements = [models.Element.OMNI] + preferred_elements

    def _sort_dice(self, dice: list[models.Element] | None = None) -> None:
        """Sort dice."""
        dice = dice or self.dice
        # omni: (0, 0, -1, 0)
        # preferred: (1, -1, -3, 3)
        # random: (1, 0, -2, 5)
        # single: (1, 0, -1, 7)
        dice.sort(
            key=lambda x: (
                x.value != models.Element.OMNI,
                -(x.value in self.preferred_elements and self.preferred_elements.index(x.value)),
                dice.count(x),
                x.value,
            )
        )

    def roll(self, amount: int = 8) -> list[models.Element]:
        """Roll dice."""
        self.dice = [random.choice(ELEMENTS) for _ in range(amount)]
        self._sort_dice()
        return self.dice

    def reroll(self, elements: list[models.Element]) -> list[models.Element]:
        """Reroll dice and return new."""
        new: list[models.Element] = []

        for element in elements:
            self.dice.remove(element)
            element = random.choice(ELEMENTS)
            new.append(element)
            self.dice.append(element)

        self._sort_dice()
        self._sort_dice(new)
        return new

    def remove(self, elements: list[models.Element]) -> None:
        """Remove dice."""
        for element in elements:
            self.dice.remove(element)
