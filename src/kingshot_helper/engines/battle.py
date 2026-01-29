from __future__ import annotations

from dataclasses import dataclass

from kingshot_helper.data import load_json
from kingshot_helper.models.enums import BattleMode


@dataclass
class FormationAdvice:
    mode: BattleMode
    infantry_count: int
    archer_count: int
    cavalry_count: int
    infantry_pct: float
    archer_pct: float
    cavalry_pct: float
    notes: str
    hero_recommendations: list[str] | None = None


def recommend_formation(mode: BattleMode, total_troops: int) -> FormationAdvice:
    """Optimal troop split for the given battle mode."""
    data = load_json("formations.json")
    ratios = data[mode.value]
    inf = int(total_troops * ratios["infantry"])
    arch = int(total_troops * ratios["archer"])
    cav = total_troops - inf - arch

    heroes = None
    hero_data = data.get("hero_recommendations", {})
    if mode == BattleMode.BEAR_HUNT:
        leaders = hero_data.get("bear_hunt_leaders", [])
        joiners = hero_data.get("bear_hunt_joiners", [])
        note_extra = hero_data.get("bear_hunt_joiner_note", "")
        heroes = leaders + joiners
        notes = ratios["notes"] + f"\n{note_extra}" if note_extra else ratios["notes"]
    else:
        notes = ratios["notes"]

    return FormationAdvice(
        mode=mode,
        infantry_count=inf,
        archer_count=arch,
        cavalry_count=cav,
        infantry_pct=ratios["infantry"],
        archer_pct=ratios["archer"],
        cavalry_pct=ratios["cavalry"],
        notes=notes,
        hero_recommendations=heroes,
    )
