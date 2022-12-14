"""Summon interface."""
import typing

from invokator import models

__all__ = ["Summon"]


class Summon(models.Summon):
    """Summon interface."""

    usage_left: int
    infused_element: models.Element | None

    def __init__(self, **kwargs: typing.Any) -> None:
        super().__init__(**kwargs)

        self.usage_left = self.usage
        self.infused_element = None
