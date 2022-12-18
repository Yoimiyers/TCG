"""TCG game loop."""
import asyncio
import random
import typing

from typing_extensions import Self

from invokator import interface, models

from . import comm, enums, utility
from .comm import events

__all__ = ["State", "main"]

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

    async def send_error(self, message: str) -> None:
        """Send an error to both players."""
        await self.mecomm(events.ErrorEvent(message=message))


async def _run_both(callback: typing.Callable[[State], typing.Awaitable[T]], state: State) -> Pair[T]:
    """Run a callback for both players."""
    return await asyncio.gather(callback(state), callback(state.reversed()))


def for_both(
    callback: typing.Callable[[State], typing.Awaitable[T]]
) -> typing.Callable[[State], typing.Awaitable[Pair[T]]]:
    """Return a callback that runs for both players."""
    return lambda state: _run_both(callback, state)


def has_all_characters_dead(state: State) -> int | None:
    """Find out who won."""
    if not state.me.alive_characters:
        return state.me.id
    if not state.opponent.alive_characters:
        return state.opponent.id

    return None


@for_both
async def choose_cards(state: State) -> None:
    """Choose cards for both players."""
    cards = state.me.draw_cards(5)

    await state.mecomm(
        events.CardDrawEvent(
            side=state.me.id,
            current_amount=state.me.hand.amount,
            current=state.me.hand.card_ids,
            amount=state.me.hand.amount,
            cards=to_ids(cards),
        )
    )
    await state.opponentcomm(
        events.CardDrawEvent(
            side=state.me.id,
            current_amount=state.me.hand.amount,
            current=None,
            amount=state.me.hand.amount,
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
    drawn_cards = state.me.draw_cards(len(discarded_cards))

    await state.mecomm(
        events.CardsChangeEvent(
            side=state.me.id,
            current_amount=state.me.hand.amount,
            current=state.me.hand.card_ids,
            amount=len(drawn_cards),
            drawn_cards=to_ids(drawn_cards),
            discarded_cards=discarded_cards,
        )
    )
    await state.opponentcomm(
        events.CardsChangeEvent(
            side=state.me.id,
            current_amount=state.me.hand.amount,
            current=None,
            amount=state.me.hand.amount,
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
        await state.send_error("No character chosen!")
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


@for_both
async def draw_cards(state: State) -> None:
    """Draw 2 cards."""
    cards = state.me.draw_cards(2)

    await state.mecomm(
        events.CardDrawEvent(
            side=state.me.id,
            current_amount=state.me.hand.amount,
            current=state.me.hand.card_ids,
            amount=len(cards),
            cards=to_ids(cards),
        )
    )
    await state.opponentcomm(
        events.CardDrawEvent(
            side=state.me.id,
            current_amount=state.me.hand.amount,
            current=None,
            amount=state.me.hand.amount,
            cards=None,
        )
    )


async def run_preparation(state: State) -> None:
    """Prepare the game."""
    await choose_cards(state)
    await choose_active_character(state)
    await roll_dice(state)


async def run_round_start(state: State) -> None:
    """Run the start of a round."""
    await state.send_both(events.StartRoundEvent(side=state.me.id))


async def run_round_end(state: State) -> None:
    """Run the end of a round."""
    await state.send_both(events.EndRoundEvent(side=state.me.id))


async def execute_effect(
    state: State,
    effect: models.Effect,
    *,
    source: models.Talent | models.CardStatus | models.Summon | None = None,
) -> None:
    """Execute an effect."""
    assert state.opponent.active_character is not None
    assert state.me.active_character is not None

    match effect:
        case models.AttackEffect():
            if effect.element:
                await state.send_error("Elements not implemented!")
            if effect.piercing:
                await state.send_error("Piercing not implemented!")
            if effect.target != models.SidelineTarget.ACTIVE_CHARACTER:
                await state.send_error("Target not implemented!")

            state.opponent.active_character.change_health(-effect.damage)
            match source:
                case models.Talent():
                    await state.send_both(
                        events.TalentEvent(
                            side=state.me.id,
                            target=state.opponent.active_character.id,
                            current=state.opponent.active_character.current_health,
                            damage=effect.damage,
                            element=effect.element,
                            source=state.me.active_character.id,
                            talent=source.id,
                        )
                    )
                case _:
                    await state.send_error(f"Unknown source for attack effect: {source!r}")
                    await state.send_both(
                        events.DamageEvent(
                            side=state.me.id,
                            target=state.opponent.active_character.id,
                            current=state.opponent.active_character.health,
                            damage=effect.damage,
                            element=effect.element,
                        )
                    )
        case _:
            await state.send_error(f"Unknown effect: {effect!r}")


async def run_attack_action(state: State) -> None:
    """Run an attack action."""
    assert state.me.active_character is not None

    talent_id = await state.mecomm(
        events.TalentRequestEvent(
            possible=to_ids(state.me.active_character.talents),
        )
    )
    if talent_id is None:
        return

    talent = state.me.active_character.get_talent(talent_id)
    if talent is None:
        await state.send_error("Invalid talent!")
        return

    dice = await state.mecomm(
        events.DiceRequestEvent(
            cost=talent.cost,
            recommended=utility.recommend_dice(state.me.dice.dice, talent.cost),
        )
    )

    if dice is None or not utility.is_enough_dice(dice, talent.cost):
        await state.send_error("Invalid dice!")
        return

    state.me.dice.remove(dice)

    await state.mecomm(
        events.DiceRemoveEvent(
            side=state.me.id,
            current_amount=len(state.me.dice.dice),
            current=state.me.dice.dice,
            amount=len(dice),
            dice=dice,
        )
    )
    await state.opponentcomm(
        events.DiceRemoveEvent(
            side=state.me.id,
            current_amount=len(state.me.dice.dice),
            current=None,
            amount=len(dice),
            dice=None,
        )
    )

    for effect in talent.effects:
        await execute_effect(state, effect, source=talent)


async def run_card_action(state: State) -> None:
    """Run a card action."""
    await state.send_error("Not implemented yet!")


async def run_tune_action(state: State) -> None:
    """Run a tune action."""
    await state.send_error("Not implemented yet!")


async def run_switch_action(state: State) -> None:
    """Run a switch action."""
    await state.send_error("Not implemented yet!")


async def run_turn(state: State) -> typing.Literal[enums.Action.CONCEDE] | None:
    """Run a turn."""
    await state.send_both(events.StartTurnEvent(side=state.me.id))

    while True:
        action = await state.mecomm(events.ActionRequestEvent())
        match action:
            case enums.Action.END:
                state.me.declared_end = True
                break
            case enums.Action.CONCEDE:
                return enums.Action.CONCEDE
            case enums.Action.ATTACK:
                await run_attack_action(state)
            case enums.Action.CARD:
                await run_card_action(state)
            case enums.Action.TUNE:
                await run_tune_action(state)
            case enums.Action.SWITCH:
                await run_switch_action(state)
            case _:
                await state.send_error("Invalid action!")
                continue

        if has_all_characters_dead(state):
            break

    await state.send_both(events.EndTurnEvent(side=state.me.id))

    return None


async def main(state: State) -> None:
    """Run a game between two players."""
    await run_preparation(state)

    # choose who starts
    if random.random() < 0.5:
        state = state.reversed()

    round_number = 1

    while True:
        state.me.declared_end = False
        state.opponent.declared_end = False

        await run_round_start(state.reversed())

        if round_number > 1:
            await draw_cards(state)

        while True:
            if state.opponent.declared_end:
                if state.me.declared_end:
                    break
            else:
                state = state.reversed()

            result = await run_turn(state)
            if result == enums.Action.CONCEDE:
                await state.send_both(events.ConcededEvent(side=state.me.id))
                return

            loser = has_all_characters_dead(state)
            if loser is not None:
                await state.send_both(events.LostEvent(side=loser))
                return

        await run_round_end(state)
        round_number += 1


async def start(players: Pair[interface.Player], comms: Pair[comm.Callback]) -> None:
    """Start a game between two players."""
    await main(State(players, comms))
