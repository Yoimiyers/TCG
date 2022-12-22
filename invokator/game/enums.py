"""TCG gameloop enusm."""
import enum


class Action(str, enum.Enum):
    """Player action enum."""

    END = "end"
    """End the round."""
    CONCEDE = "concede"
    """Concede the game."""
    ATTACK = "attack"
    """Use a character talent."""
    CARD = "card"
    """Play a card."""
    TUNE = "tune"
    """Change a dice element."""
    SWITCH = "switch"
    """Switch the active character."""
