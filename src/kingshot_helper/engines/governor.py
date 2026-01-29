from __future__ import annotations

from dataclasses import dataclass

from kingshot_helper.data import load_json

TIER_ORDER = ["green", "blue", "purple", "mythic", "red"]


@dataclass
class GovGearResult:
    current_tier: str
    current_stars: int
    target_tier: str
    target_stars: int
    satin_needed: int
    threads_needed: int
    visions_needed: int
    satin_deficit: int
    threads_deficit: int
    visions_deficit: int
    power_at_target: int | None


@dataclass
class CharmResult:
    current_level: int
    target_level: int
    guides_needed: int
    designs_needed: int
    guides_deficit: int
    designs_deficit: int
    breakdown: list[dict]


def _tier_star_index(tier: str, star: int) -> int:
    return TIER_ORDER.index(tier) * 4 + star


def calc_governor_gear(
    current_tier: str,
    current_stars: int,
    target_tier: str,
    target_stars: int,
    satin_owned: int = 0,
    threads_owned: int = 0,
    visions_owned: int = 0,
) -> GovGearResult:
    """Sum materials from current to target tier+star."""
    data = load_json("governor_gear.json")
    tiers = data["tiers"]

    current_idx = None
    target_idx = None
    for i, entry in enumerate(tiers):
        if entry["tier"] == current_tier and entry["star"] == current_stars:
            current_idx = i
        if entry["tier"] == target_tier and entry["star"] == target_stars:
            target_idx = i

    if current_idx is None or target_idx is None or target_idx <= current_idx:
        return GovGearResult(
            current_tier,
            current_stars,
            target_tier,
            target_stars,
            0,
            0,
            0,
            0,
            0,
            0,
            None,
        )

    satin = sum(tiers[i]["satin"] for i in range(current_idx + 1, target_idx + 1))
    threads = sum(tiers[i]["threads"] for i in range(current_idx + 1, target_idx + 1))
    visions = sum(tiers[i]["visions"] for i in range(current_idx + 1, target_idx + 1))
    power = tiers[target_idx].get("power")

    return GovGearResult(
        current_tier,
        current_stars,
        target_tier,
        target_stars,
        satin,
        threads,
        visions,
        max(0, satin - satin_owned),
        max(0, threads - threads_owned),
        max(0, visions - visions_owned),
        power,
    )


def calc_governor_charm(
    current: int,
    target: int,
    guides_owned: int = 0,
    designs_owned: int = 0,
) -> CharmResult:
    """Sum charm materials from current to target level."""
    data = load_json("governor_charms.json")
    levels = {e["level"]: e for e in data["levels"]}

    breakdown = []
    guides_total, designs_total = 0, 0
    for lv in range(current + 1, target + 1):
        entry = levels.get(lv)
        if entry:
            guides_total += entry["guides"]
            designs_total += entry["designs"]
            breakdown.append(entry)

    return CharmResult(
        current,
        target,
        guides_total,
        designs_total,
        max(0, guides_total - guides_owned),
        max(0, designs_total - designs_owned),
        breakdown,
    )
