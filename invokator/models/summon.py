"""TCG summons."""
import pydantic

from .effect import Effect


class Summon(pydantic.BaseModel):
    """TCG summon."""

    id: str
    usage: int
    effects: list[Effect]
