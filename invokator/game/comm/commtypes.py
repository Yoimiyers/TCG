"""Types for communication."""
import typing

from . import events

__all__ = ["Callback"]

T = typing.TypeVar("T")


class Callback(typing.Protocol):
    """A callback for events."""

    async def __call__(self, event: events.BaseEvent[T]) -> T | None:
        """Send an event."""
