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

    def _sort_dice(self) -> None:
        """Sort dice."""
        # omni: (0, 0, 0)
        # preferred: (1, -1, 3)
        # random: (1, 0, 4)
        self.dice.sort(
            key=lambda x: (
                x.value != models.Element.OMNI,
                -(
                    x.value in self.preferred_elements
                    and self.preferred_elements.index(x.value)
                ),
                x.value,
            )
        )

    def roll(self, amount: int = 8) -> None:
        """Roll dice."""
        self.dice = [random.choice(ELEMENTS) for _ in range(amount)]

    def reroll(self, indices: list[int]) -> list[models.Element]:
        """Reroll dice and return new."""
        new: list[models.Element] = []

        for index in indices:
            element = random.choice(ELEMENTS)
            new.append(element)
            self.dice[index] = element

        return new
