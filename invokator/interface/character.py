"""Character interface."""
import typing

import pydantic

from invokator import models

__all__ = ["Character"]

NO_DEFAULT: typing.Any = pydantic.Field(default_factory=lambda: pydantic.fields.Undefined)


class CharacterStatus(models.CardStatus):
    """Character effect interface."""

    duration: int = NO_DEFAULT

    def __init__(self, **kwargs: typing.Any) -> None:
        super().__init__(**kwargs)

        self.duration = self.usage


class Character(models.Character):
    """Character interface."""

    current_health: int = NO_DEFAULT
    current_energy: int = 0
    afflicted_elements: list[models.Element] | None = []
    infused_element: models.Element | None = None

    status: list[CharacterStatus] = []
    equipped_weapon: models.WeaponCard | None = None
    equipped_artifact: models.ArtifactCard | None = None

    def __init__(self, **kwargs: typing.Any) -> None:
        super().__init__(**kwargs)

        self.current_health = self.health

    def change_health(self, amount: int) -> None:
        """Change health."""
        self.current_health = min(self.health, max(0, self.current_health + amount))
