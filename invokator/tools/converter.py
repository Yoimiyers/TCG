"""Convert raw data to carddata format usable by TCG."""
import typing

ELEMENTS: dict[str, str] = {
    "物理": "physical",
    "火": "Pyro",
    "水": "Hydro",
    "冰": "Cryo",
    "雷": "Electro",
    "岩": "Geo",
    "風": "Anemo",
    "草": "Dendro",
    "萬能": "omni",
}

ET_ELEMENTS: dict[str, str] = {
    "ETIce": "Cryo",
    "ETFire": "Pyro",
    "ETWater": "Hydro",
    "ETWind": "Anemo",
    "ETRock": "Geo",
    "ETThunder": "Electro",
    "ETGrass": "Dendro",
}

DICE_ELEMENTS: dict[str, str | None] = {
    "1": "Energy",
    "3": "Omni",
    "10": None,
    "11": "Cryo",
    "12": "Hydro",
    "13": "Pyro",
    "14": "Electro",
    "15": "Geo",
    "16": "Dendro",
    "17": "Anemo",
}

WEAPON_TYPES: dict[str, str] = {
    "單手劍": "Sword",
    "雙手劍": "Claymore",
    "弓": "Bow",
    "法器": "Catalyst",
    "長柄武器": "Polearm",
    "其他武器": "Other",
}

LOCATIONS: dict[str, str] = {
    "蒙德": "Mondstadt",
    "璃月": "Liyue",
    "稻妻": "Inazuma",
    "須彌": "Sumeru",
    "愚人眾": "Fatui",
    "魔物": "Monster",
}

SKILL_TYPES: dict[str, str] = {
    "普通攻擊": "normal",
    "元素爆發": "burst",
    "元素戰技": "skill",
    "被動技能": "passive",
}


def convert_to_carddata(raw_data: typing.Dict[str, typing.Any]) -> typing.Dict[str, typing.Any]:
    """Convert raw card data to carddata format usable by TCG."""
    # characters
    characters: typing.Dict[str, typing.Any] = {}
    for card in raw_data["role_card_infos"]:
        name = card["name"]

        # basic information
        c = characters[name] = {
            "id": card["id"],
            "name": name,
            "element": ET_ELEMENTS[card["element_type"]],
            "weapon": WEAPON_TYPES[card["weapon"]],
            "location": LOCATIONS[card["belong_to"][0]],
        }
        c["talents"] = []

        # skills
        for skill in card["role_skill_infos"]:
            talent = {"id": skill["id"], "name": skill["name"]}

            talent_cost: typing.List[typing.Dict[str, typing.Optional[typing.Union[int, str]]]] = []
            for cost in skill["skill_costs"]:
                if not cost["cost_icon"]:
                    continue
                talent_cost.append({"element": DICE_ELEMENTS[cost["cost_icon"]], "amount": int(cost["cost_num"])})
            talent["cost"] = talent_cost

            talent["type"] = SKILL_TYPES[skill["type"][0]]
            if talent["type"] == "burst":
                for cost in talent["cost"]:
                    if cost["element"] == "Energy":
                        c["energy"] = cost["amount"]
                        break

            c["talents"].append(talent)

    return characters
