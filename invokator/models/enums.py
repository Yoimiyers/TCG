"""TCG enums."""
import enum


class Element(str, enum.Enum):
    """Elemental type of a character."""

    ANEMO = "Anemo"
    """Anemo."""
    CRYO = "Cryo"
    """Cryo."""
    DENDRO = "Dendro"
    """Dendro."""
    ELECTRO = "Electro"
    """Electro."""
    GEO = "Geo"
    """Geo."""
    HYDRO = "Hydro"
    """Hydro."""
    PYRO = "Pyro"
    """Pyro."""

    OMNI = "omni"
    """Omnidice. 
    
    Used for cards that can be used with any dice.
    """

    PHYSICAL = "physical"
    """Physical damage type."""

    INFUSED = "infused"
    """Placeholder for the infused element."""


class ReactionType(str, enum.Enum):
    """Reaction types."""

    VAPORIZE = "vaporize"
    """Pyro + Hydro"""
    MELT = "melt"
    """Pyro + Cryo"""
    ELECTROCHARGED = "electrocharged"
    """Electro + Hydro"""
    OVERLOAD = "overload"
    """Electro + Pyro"""
    SUPERCONDUCT = "superconduct"
    """Electro + Cryo"""
    FROZEN = "frozen"
    """Hydro + Cryo"""
    BURNING = "burning"
    """Denro + Pyro"""
    BLOOM = "bloom"
    """Dendro + Hydro"""
    QUICKEN = "quicken"
    """Dendro + Electro"""
    SWIRL = "swirl"
    """Anemo + Any"""
    CRYSTALIZE = "crystalize"
    """Geo + Any"""


class CardType(str, enum.Enum):
    """Type of a card."""

    EVENT = "event"
    """Event card."""
    SUPPORT = "support"
    """Support card."""
    FOOD = "food"
    """Food card."""
    EQUIPMENT = "equipment"
    """Equipment card."""
    CHARACTER = "character"
    """Character card."""


class EquipmentType(str, enum.Enum):
    """Type of an equipment card."""

    ARTIFACT = "artifact"
    """Artifact card."""
    WEAPON = "weapon"
    """Weapon card."""


class TalentType(str, enum.Enum):
    """Type of a character's talent."""

    NORMAL = A = "normal"
    """Normal attack."""
    SKILL = E = "skill"
    """Skill talent."""
    BURST = Q = "burst"
    """Burst talent."""
    PASSIVE = "passive"
    """Passive talent."""


class EffectType(str, enum.Enum):
    """Effect type of a character's talent."""

    ATTACK = "attack"
    """Attack an opponent character."""
    HEAL = "heal"
    """Heal a friendly character."""
    SUMMON = "summon"
    """Summon a summon."""
    EFFECT = "effect"
    """Apply an effect to a character."""
    INFUSE = "infuse"
    """Infuse the character with an element."""
    SWITCH = "switch"
    """Switch the current active character."""
    FORCESWITCH = "forceswitch"
    """Switch the opponent's active character."""

    BUFF = "buff"
    """Buff a character's attack."""
    CLEAR = "clear"
    """Clear this effect from a character."""
    DISCOUNT = "discount"
    """Reduce the dice cost of an action."""
    DECREMENT = "decrement"
    """Decrement the usages of this effect."""
    DRAW = "draw"
    """Draw a card."""
    ADDDICE = "adddice"
    """Add a dice to the player."""
    DESTROY = "destroy"
    """Destroy a sideline card."""
    EXTEND = "extend"
    """Extend the duration of a card."""
    SWAP = "swap"
    """Swap the equipment of two characters"""
    ENERGY = "energy"
    """Add or remove energy from a character."""


class EffectTrigger(str, enum.Enum):
    """Trigger of an effect."""

    ATTACK = "attack"
    """Trigger on attack."""

    DEPLETED = "depleted"
    """Trigger when the effect is depleted."""
    START = "start"
    """Trigger on start of a round."""
    END = "end"
    """Trigger on end of round."""
    SWITCH = "switch"
    """Trigger on character switch."""

    REACTION = "reaction"
    """Trigger on a reaction."""

    DEPLOY = "deploy"
    """Trigger on effect or summon deploy."""


class CardEffectAttachType(str, enum.Enum):
    """Type of card effect attachment."""

    STATIC = "static"
    """Effect always stays with this character."""
    DYNAMIC = "dynamic"
    """Effect moves with the active character."""


class SidelineTarget(str, enum.Enum):
    """Target of a destroy card."""

    SUMMON = "summon"
    """Target a summon."""

    CHARACTER = "character"
    """Target a character."""

    ACTIVE_CHARACTER = "active_character"
    """Target the active character."""


class SidelineLocation(str, enum.Enum):
    """Location of a destroy card."""

    ANY = "any"
    FRIEND = "friend"
    ENEMY = "enemy"
