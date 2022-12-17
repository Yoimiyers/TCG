"""Dice game utilities."""
from invokator import models

__all__ = ["is_enough_dice", "recommend_dice"]

# TODO: Make this smarter and cleaner


def is_enough_dice(dice: list[models.Element], cost: list[models.DiceCost]) -> bool:
    """Check if there are enough dice for a cost."""
    return recommend_dice(dice, cost) is not None


def recommend_dice(
    dice: list[models.Element],
    cost: list[models.DiceCost],
) -> list[models.Element] | None:
    """Recommend dice to use for a cost.

    Dice should already be sorted.
    """
    element: models.Element | None = None  # null = same, omni = any
    element_amount: int = 0
    omni_amount: int = 0

    for dice_cost in cost:
        if dice_cost.element == models.Element.OMNI:
            omni_amount = dice_cost.amount
        else:
            element = dice_cost.element
            element_amount = dice_cost.amount

    if element_amount + omni_amount > len(dice):
        return None

    recommended: list[models.Element] = []

    present_omnis = dice.count(models.Element.OMNI)
    omnilessdice = [die for die in dice if die != models.Element.OMNI]

    if element is None:
        # depends on dict ordering
        priority: dict[models.Element, int] = {}
        for die_element in omnilessdice:
            priority[die_element] = priority.get(die_element, 0) + 1

        for die_element, die_amount in reversed(priority.items()):
            if die_amount + present_omnis >= element_amount:
                used_colored = min(die_amount, element_amount)
                recommended.extend([die_element] * used_colored)
                recommended.extend([models.Element.OMNI] * (element_amount - used_colored))
                break
        else:
            return None

    elif element is not None:
        die_element = element
        die_amount = sum(1 for die in omnilessdice if die == element)
        if die_amount + present_omnis < element_amount:
            return None

        used_colored = min(die_amount, element_amount)
        recommended.extend([die_element] * used_colored)
        recommended.extend([models.Element.OMNI] * (element_amount - used_colored))

    # use the unrecommended dice
    recommended.extend(dice[-omni_amount:])

    return recommended
