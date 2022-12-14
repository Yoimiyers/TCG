"""TCG gameloop enusm."""
import enum


class Action(str, enum.Enum):
    """Player action enum."""

    CARD = "card"
    """Play a card."""
    DICE = "dice"
    """Change a dice element."""
    ATTACK = "attack"
    """Use a character talent."""
    END = "end"
    """End the round."""
    SWITCH = "switch"
    """Switch the active character."""
