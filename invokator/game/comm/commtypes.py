"""Types for communication."""
import typing

from . import events

__all__ = ["Callback"]

T = typing.TypeVar("T")

Callback = typing.Callable[[events.BaseEvent[T]], typing.Awaitable[T | None]]
