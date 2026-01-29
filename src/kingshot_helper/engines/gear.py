from __future__ import annotations

from dataclasses import dataclass

from kingshot_helper.data import load_json
from kingshot_helper.models.enums import Rarity


@dataclass
class EnhanceResult:
    current_level: int
    target_level: int
    rarity: Rarity
    max_level: int
    total_xp: int
    capped: bool


@dataclass
class ForgeResult:
    current_level: int
    target_level: int
    total_hammers: int
    total_mythic_gears: int
    stat_bonus_percent: float
    breakdown: list[dict]


@dataclass
class MithrilResult:
    current_level: int
    target_level: int
    total_mithril: int
    total_mythic_gears: int
    blocks: list[dict]


def calc_enhancement_xp(current: int, target: int, rarity: Rarity = Rarity.MYTHIC) -> EnhanceResult:
    """Total enhancement XP for gear level range, capped by rarity."""
    data = load_json("gear_enhancement.json")
    cap = data["rarity_caps"][rarity.value]
    effective_target = min(target, cap)
    capped = target > cap
    xp_table = data["xp_per_level"]
    total = sum(
        xp_table[lv] for lv in range(current + 1, effective_target + 1) if lv < len(xp_table)
    )
    return EnhanceResult(current, effective_target, rarity, cap, total, capped)


def calc_forgehammer(current: int, target: int) -> ForgeResult:
    """Forgehammers and mythic gears for mastery level range."""
    data = load_json("forgehammer.json")
    levels = {e["level"]: e for e in data["levels"]}
    breakdown = []
    total_h, total_g = 0, 0
    for lv in range(current + 1, target + 1):
        entry = levels.get(lv)
        if entry:
            total_h += entry["hammers"]
            total_g += entry["mythic_gears"]
            breakdown.append(entry)
    bonus = target * data["stat_bonus_per_level"] * 100
    return ForgeResult(current, target, total_h, total_g, bonus, breakdown)


def calc_mithril_upgrade(current: int, target: int) -> MithrilResult:
    """Mithril and mythic gear costs for red gear level blocks."""
    data = load_json("gear_mithril.json")
    blocks = [
        b for b in data["red_blocks"] if b["from_level"] >= current and b["to_level"] <= target
    ]
    total_m = sum(b["mithril"] for b in blocks)
    total_g = sum(b["mythic_gears"] for b in blocks)
    return MithrilResult(current, target, total_m, total_g, blocks)
