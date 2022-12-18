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
    """Omnidie.

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
    WEAPON = "weapon"
    """Weapon card."""
    ARTIFACT = "artifact"
    """Artifact card."""
    CHARACTER = "character"
    """Character card."""


class EquipmentType(str, enum.Enum):
    """Type of an equipment card."""

    ARTIFACT = "artifact"
    """Artifact card."""
    WEAPON = "weapon"
    """Weapon card."""


class WeaponType(str, enum.Enum):
    """Type of a weapon card."""

    SWORD = "Sword"
    """Sword."""
    CLAYMORE = "Claymore"
    """Claymore."""
    POLEARM = "Polearm"
    """Polearm."""
    BOW = "Bow"
    """Bow."""
    CATALYST = "Catalyst"
    """Catalyst."""
    OTHER = "Other"
    """Monster's weapon."""


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

    NONE = "none"
    """No effect."""

    ATTACK = "attack"
    """Attack an opponent character."""
    HEAL = "heal"
    """Heal a friendly character."""
    SUMMON = "summon"
    """Summon a summon."""
    STATUS = "status"
    """Apply an effect to a character."""
    INFUSE = "infuse"
    """Infuse the character with an element."""
    SWITCH = "switch"
    """Switch the current active character."""

    BUFF = "buff"
    """Buff a character's attack."""
    CLEAR = "clear"
    """Clear this effect from a character."""
    DISCOUNT = "discount"
    """Reduce the dice cost of an action."""
    DECREMENT = "decrement"
    """Decrement the usages of this status."""
    DRAW = "draw"
    """Draw a card."""
    ADDDICE = "adddice"
    """Add a dice to the player."""
    DESTROY = "destroy"
    """Destroy a sideline card."""
    EXTEND = "extend"
    """Extend the duration of a card."""
    SHIFT = "shift"
    """Shift the equipment of two characters"""
    ENERGY = "energy"
    """Add or remove energy from a character."""
    QUICK = "quick"
    """Make an effect a quick action."""
    PROTECT = "protect"
    """Reduces the damage of an attack."""


class EffectTriggerType(str, enum.Enum):
    """Trigger of an effect."""

    ATTACK = "attack"
    """Trigger on attack."""
    DAMAGE = "damage"
    """Trigger on damage above a threshold."""

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


class CardStatusAttachType(str, enum.Enum):
    """Type of card status attachment."""

    STATIC = "static"
    """Status always stays with this character."""
    DYNAMIC = "dynamic"
    """Status moves with the active character."""
    TEMPORARY = "temporary"
    """Status is removed when the character is switched."""


class SidelineTarget(str, enum.Enum):
    """Target of a destroy card."""

    SUMMON = "summon"
    """Target a summon."""

    CHARACTER = "character"
    """Target a character."""

    ACTIVE_CHARACTER = "active_character"
    """Target the active character."""

    INACTIVE_CHARACTER = "inactive_character"
    """Target the inactive character."""


class SidelineLocation(str, enum.Enum):
    """Location of a destroy card."""

    ANY = "any"
    FRIEND = "friend"
    ENEMY = "enemy"


class CardDirection(str, enum.Enum):
    """Position of a card."""

    LEFT = "left"
    RIGHT = "right"
