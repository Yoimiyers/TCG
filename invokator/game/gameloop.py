"""TCG game loop."""
import asyncio
import typing

from typing_extensions import Self

from invokator import interface

from . import comm
from .comm import events

T = typing.TypeVar("T")

Pair = typing.Tuple[T, T]


class IDModel(typing.Protocol):
    """Protocol for models with an ID."""

    id: int


def to_ids(items: typing.Iterable[IDModel]) -> list[int]:
    """Return a list of IDs."""
    return [item.id for item in items]


class State:
    """The game state."""

    players: Pair[interface.Player]
    """The players."""

    comms: Pair[comm.Callback]
    """The communication channels."""

    def __init__(self, players: Pair[interface.Player], comms: Pair[comm.Callback]) -> None:
        self.players = players
        self.comms = comms

    def reversed(self) -> Self:
        """Return a reversed state."""
        return State(self.players[::-1], self.comms[::-1])

    @property
    def me(self) -> interface.Player:
        """The current player."""
        return self.players[0]

    @property
    def mecomm(self) -> comm.Callback:
        """The current player's communication channel."""
        return self.comms[0]

    @property
    def opponent(self) -> interface.Player:
        """The opponent."""
        return self.players[1]

    @property
    def opponentcomm(self) -> comm.Callback:
        """The opponent's communication channel."""
        return self.comms[1]

    async def send_both(self, event: events.Event) -> None:
        """Send an event to both players."""
        await asyncio.gather(self.comms[0](event), self.comms[1](event))


async def _run_both(callback: typing.Callable[[State], typing.Awaitable[T]], state: State) -> Pair[T]:
    """Run a callback for both players."""
    return await asyncio.gather(callback(state), callback(state.reversed()))


def for_both(
    callback: typing.Callable[[State], typing.Awaitable[T]]
) -> typing.Callable[[State], typing.Awaitable[Pair[T]]]:
    """Return a callback that runs for both players."""
    return lambda state: _run_both(callback, state)


def has_won(state: State) -> int | None:
    """Find out who won."""
    if not state.me.alive_characters:
        return state.opponent.id
    if not state.opponent.alive_characters:
        return state.me.id

    return None


@for_both
async def choose_cards(state: State) -> None:
    """Choose cards for both players."""
    cards = state.me.draw_cards(5)

    await state.mecomm(
        events.CardDrawEvent(
            side=state.me.id,
            current_amount=state.me.deck.amount,
            current=state.me.deck.card_ids,
            amount=state.me.deck.amount,
            cards=to_ids(cards),
        )
    )
    await state.opponentcomm(
        events.CardDrawEvent(
            side=state.me.id,
            current_amount=state.me.deck.amount,
            current=None,
            amount=state.me.deck.amount,
            cards=None,
        )
    )

    discarded_cards = await state.mecomm(events.CardsChangeRequestEvent(possible=to_ids(cards)))
    if discarded_cards is None:
        discarded_cards = []

    for card_id in discarded_cards:
        card = state.me.hand.remove_card(card_id)
        state.me.deck.cards.append(card)

    state.me.deck.shuffle()
    drawn_cards = state.me.draw_cards(5 - len(discarded_cards))

    await state.mecomm(
        events.CardsChangeEvent(
            side=state.me.id,
            current_amount=state.me.deck.amount,
            current=state.me.deck.card_ids,
            amount=len(drawn_cards),
            drawn_cards=to_ids(drawn_cards),
            discarded_cards=discarded_cards,
        )
    )
    await state.opponentcomm(
        events.CardsChangeEvent(
            side=state.me.id,
            current_amount=state.me.deck.amount,
            current=None,
            amount=state.me.deck.amount,
            drawn_cards=None,
            discarded_cards=None,
        )
    )


@for_both
async def choose_active_character(state: State) -> None:
    """Choose an active character for both players."""
    character = await state.mecomm(
        events.CharacterRequestEvent(
            possible=to_ids(state.me.characters),
            possible_enemy=None,
        )
    )
    if character is None:
        await state.mecomm(events.ErrorEvent(message="No character chosen!"))
        character = state.me.characters[0].id

    state.me.switch_character(character)

    await state.send_both(events.SwitchEvent(side=state.me.id, target=character, previous=None))


@for_both
async def roll_dice(state: State) -> None:
    """Roll the dice for both players."""
    dice = state.me.dice.roll(8)

    await state.mecomm(
        events.DiceAddEvent(
            side=state.me.id,
            current_amount=len(dice),
            current=dice,
            amount=len(dice),
            dice=dice,
        )
    )
    await state.opponentcomm(
        events.DiceAddEvent(
            side=state.me.id,
            current_amount=len(dice),
            current=None,
            amount=len(dice),
            dice=None,
        )
    )

    rerolled = await state.mecomm(events.DiceChangeRequestEvent(possible=dice))

    if rerolled:
        new = state.me.dice.reroll(rerolled)
    else:
        rerolled = []
        new = []

    await state.mecomm(
        events.DiceRerollEvent(
            side=state.me.id,
            current_amount=len(dice),
            current=dice,
            amount=len(new),
            rerolled_dice=rerolled,
            new_dice=new,
        )
    )
    await state.opponentcomm(
        events.DiceRerollEvent(
            side=state.me.id,
            current_amount=len(dice),
            current=None,
            amount=len(new),
            rerolled_dice=None,
            new_dice=None,
        )
    )


async def run_preparation(state: State) -> None:
    """Prepare the game."""
    await choose_cards(state)
    await choose_active_character(state)
    await roll_dice(state)


async def run_round(state: State) -> None:
    """Run a round."""
    await state.send_both(events.StartRoundEvent(side=state.me.id))

    await state.send_both(events.EndRoundEvent(side=state.me.id))


async def main(state: State) -> None:
    """Run a game between two players."""
    await run_preparation(state)

    while True:
        await run_round(state)

        if victor := has_won(state):
            break

    await state.send_both(events.EndGameEvent(side=victor))


async def start(players: Pair[interface.Player], comms: Pair[comm.Callback]) -> None:
    """Start a game between two players."""
    await main(State(players, comms))
