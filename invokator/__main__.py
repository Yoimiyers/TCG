"""Debug the TCG."""
import asyncio
import pprint
import typing

import pydantic

import invokator

T = typing.TypeVar("T")

CHARACTER_IDS = (1301, 1103, 1501)


def create_event_callback(id: int) -> invokator.game.Callback:
    """Create a callback for an event."""

    async def event_callback(event: invokator.game.BaseEvent[typing.Any]) -> typing.Any:
        # print the recieved data
        print()  # noqa: T201
        print(id, event.__repr_name__(), event.json(separators=(", ", ": ")))  # noqa: T201

        try:
            response_type: typing.Any = event.__orig_bases__[0].__args__[0]  # type: ignore
            response_type_origin = typing.get_origin(response_type) or response_type
        except Exception:
            return None

        if response_type in (None, type(None)):
            return None

        # ask for the response if needed
        while True:
            print(response_type, end=" : ")  # noqa: T201
            raw_response = input().strip()

            if raw_response == "view":
                print("====================")  # noqa: T201
                pprint.pprint(state.players[0].dict(), indent=2)  # noqa: T203
                print("--------------------")  # noqa: T201
                pprint.pprint(state.players[1].dict(), indent=2)  # noqa: T203
                print("====================")  # noqa: T201
                continue

            if response_type_origin == list:
                raw_response = raw_response.split()

            if not raw_response:
                return None

            try:
                return pydantic.parse_obj_as(response_type, raw_response)
            except Exception as e:
                print(e)  # noqa: T201
                continue

    return event_callback


def create_default_player(id: int) -> invokator.interface.Player:
    """Create a default player."""
    characters = [
        invokator.interface.Character.parse_obj(character)
        for character in invokator.models.CHARACTERS
        if character.id in CHARACTER_IDS
    ]
    cards = invokator.models.CARDS
    return invokator.interface.Player(id=id, characters=characters, deck=cards)


state: invokator.game.State = invokator.game.State(
    (create_default_player(111), create_default_player(222)),
    (create_event_callback(111), create_event_callback(222)),
)

if __name__ == "__main__":
    asyncio.run(invokator.game.main(state))
