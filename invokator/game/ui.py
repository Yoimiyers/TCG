"""ABC for game objects."""
import abc

from invokator import interface, models

from . import enums


class UserInterface(abc.ABC):
    """Basic interface between the user and the game.

    Any action may be cancelled with None.
    """

    player: interface.Player
    enemy: interface.Player

    @abc.abstractmethod
    async def show_effect(self, source: str, effect: models.Effect) -> None:
        """Show what happened in-game to the user.

        Source is the card's ID.
        """

    @abc.abstractmethod
    async def choose_action(self) -> enums.Action:
        """Choose an action to do."""

    @abc.abstractmethod
    async def choose_card(self) -> str | None:
        """Choose a card to play.

        Return the object's ID.
        """

    @abc.abstractmethod
    async def choose_talent(self) -> str | None:
        """Choose a talent to use.

        Return the object's ID.
        """

    @abc.abstractmethod
    async def choose_character(self, location: models.SidelineLocation) -> str | None:
        """Choose a character from the gameboard.

        Returns the object's ID.
        """

    @abc.abstractmethod
    async def choose_summon(self, location: models.SidelineLocation) -> str | None:
        """Choose a summon from the gameboard.

        Returns the object's ID.
        """

    @abc.abstractmethod
    async def choose_dice(self, amount: int, dice: list[models.DiceCost]) -> list[models.Element] | None:
        """Chose an amount of dice from the dice pool.

        Must be equivalent to the cost.
        """
