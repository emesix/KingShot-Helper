from __future__ import annotations

from dataclasses import dataclass

from kingshot_helper.data import load_json
from kingshot_helper.models.enums import PetRarity


@dataclass
class PetLevelResult:
    current: int
    target: int
    effective_target: int
    capped: bool
    advancements: list[dict]


def calc_pet_level(current: int, target: int, rarity: PetRarity) -> PetLevelResult:
    """Pet leveling with advancement milestones."""
    data = load_json("pet_levels.json")
    cap = data["rarity_caps"][rarity.value]
    effective = min(target, cap)
    capped = target > cap
    interval = data["advancement_interval"]
    advancement_data = data["advancement_items"]

    advancements = []
    for lv in range(current + 1, effective + 1):
        if lv % interval == 0:
            items = advancement_data.get(str(lv), {})
            advancements.append({"level": lv, "items": items})

    return PetLevelResult(current, target, effective, capped, advancements)
