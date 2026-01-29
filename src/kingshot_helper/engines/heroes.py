from __future__ import annotations

from dataclasses import dataclass

from kingshot_helper.data import load_json


@dataclass
class XPResult:
    current_level: int
    target_level: int
    total_xp: int
    tc_required: int
    breakdown: list[tuple[int, int]]


@dataclass
class ShardResult:
    current_stars: int
    target_stars: int
    shards_needed: int
    shards_owned: int
    shards_deficit: int
    per_star: list[tuple[int, int]]


def _tc_for_level(level: int) -> int:
    data = load_json("hero_xp.json")
    tc_map = data["tc_per_level"]
    result = 4
    for lv_str, tc in sorted(tc_map.items(), key=lambda x: int(x[0])):
        if int(lv_str) <= level:
            result = tc
    return result


def calc_hero_xp(current: int, target: int) -> XPResult:
    """Total XP needed from current level to target level."""
    data = load_json("hero_xp.json")
    xp_table = data["xp_per_level"]
    breakdown = [(lv, xp_table[lv]) for lv in range(current + 1, min(target + 1, len(xp_table)))]
    total = sum(xp for _, xp in breakdown)
    tc = _tc_for_level(target)
    return XPResult(current, target, total, tc, breakdown)


def calc_shards(
    current_stars: int,
    target_stars: int,
    shards_owned: int = 0,
    hero_name: str = "default",
) -> ShardResult:
    """Shards needed from current to target star level."""
    data = load_json("hero_shards.json")
    per_star = data["shards_per_star"]
    details = []
    total = 0
    for s in range(current_stars + 1, target_stars + 1):
        cost = per_star[str(s)]
        details.append((s, cost))
        total += cost
    deficit = max(0, total - shards_owned)
    return ShardResult(current_stars, target_stars, total, shards_owned, deficit, details)


def drill_camp_xp(primary_xp: int) -> int:
    """80% XP spillover to drill camp heroes."""
    data = load_json("hero_xp.json")
    return int(primary_xp * data["drill_camp_spillover"])
