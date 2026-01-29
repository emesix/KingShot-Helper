from __future__ import annotations

from dataclasses import dataclass

from kingshot_helper.engines.buildings import tc_unlocks
from kingshot_helper.engines.heroes import calc_shards
from kingshot_helper.models.enums import Rarity
from kingshot_helper.models.profile import UserProfile


@dataclass
class Recommendation:
    domain: str
    priority: int
    action: str
    reason: str
    impact: str


def get_recommendations(profile: UserProfile, top_n: int = 5) -> list[Recommendation]:
    """Evaluate profile and return prioritized upgrade suggestions."""
    recs: list[Recommendation] = []
    _check_tc_unlocks(profile, recs)
    _check_hero_priorities(profile, recs)
    _check_gear_priorities(profile, recs)
    _check_governor(profile, recs)
    _check_general(profile, recs)
    recs.sort(key=lambda r: r.priority)
    return recs[:top_n]


def _check_tc_unlocks(profile: UserProfile, recs: list[Recommendation]) -> None:
    info = tc_unlocks(profile.town_center_level)
    if info.next_unlock:
        level, feature = info.next_unlock
        recs.append(
            Recommendation(
                domain="building",
                priority=1,
                action=f"Upgrade Town Center to {level}",
                reason=f"Unlocks: {feature}",
                impact="Gate unlock — enables new game systems",
            )
        )


def _check_hero_priorities(profile: UserProfile, recs: list[Recommendation]) -> None:
    if not profile.heroes:
        recs.append(
            Recommendation(
                domain="hero",
                priority=2,
                action="Set up hero data in your profile",
                reason="Hero progression is the highest-impact investment",
                impact="Can't give hero advice without hero data",
            )
        )
        return

    for hero in profile.heroes:
        if hero.stars < 5:
            result = calc_shards(hero.stars, hero.stars + 1, hero.shards_owned)
            if result.shards_deficit == 0:
                recs.append(
                    Recommendation(
                        domain="hero",
                        priority=2,
                        action=f"Ascend {hero.name} to {hero.stars + 1}★",
                        reason=f"You have enough shards ({result.shards_needed} needed)",
                        impact="Major stat boost + skill unlock",
                    )
                )
            else:
                recs.append(
                    Recommendation(
                        domain="hero",
                        priority=5,
                        action=(
                            f"Collect {result.shards_deficit} more shards"
                            f" for {hero.name} {hero.stars + 1}★"
                        ),
                        reason=f"Need {result.shards_needed} total, have {hero.shards_owned}",
                        impact="Next star ascension",
                    )
                )
        if hero.level < 80 and profile.town_center_level >= 26:
            recs.append(
                Recommendation(
                    domain="hero",
                    priority=3,
                    action=f"Level {hero.name} to 80 (currently {hero.level})",
                    reason="TC 26+ allows hero level 80. 80% XP spills to Drill Camp",
                    impact="Max hero stats + drill camp benefit",
                )
            )


def _check_gear_priorities(profile: UserProfile, recs: list[Recommendation]) -> None:
    for hero in profile.heroes:
        if not hero.gear:
            continue
        for slot, gear in hero.gear.items():
            if gear.rarity == Rarity.MYTHIC and gear.mastery_level < 10:
                recs.append(
                    Recommendation(
                        domain="gear",
                        priority=4,
                        action=f"Forge {hero.name}'s {slot.value} to mastery 10",
                        reason="Mastery 10 required for Red gear imbue (+100% stats)",
                        impact=f"Currently mastery {gear.mastery_level}",
                    )
                )


def _check_governor(profile: UserProfile, recs: list[Recommendation]) -> None:
    if profile.town_center_level >= 22:
        gg = profile.governor_gear
        if gg.tier in (Rarity.GREEN, Rarity.BLUE):
            recs.append(
                Recommendation(
                    domain="governor",
                    priority=3,
                    action=f"Upgrade Governor Gear (currently {gg.tier.value} {gg.stars}★)",
                    reason="Governor Gear provides massive global troop buffs",
                    impact="Priority: Infantry set first, then Archer, then Cavalry",
                )
            )

    if profile.town_center_level >= 25:
        gc = profile.governor_charm
        if gc.level < 10:
            recs.append(
                Recommendation(
                    domain="governor",
                    priority=4,
                    action=f"Level Governor Charm to 10 (currently {gc.level})",
                    reason="Charms give large stat boosts, early levels are cheap",
                    impact="Big returns on investment at lower levels",
                )
            )


def _check_general(profile: UserProfile, recs: list[Recommendation]) -> None:
    if not recs:
        recs.append(
            Recommendation(
                domain="general",
                priority=10,
                action="Fill out your profile with more data",
                reason="More data = better recommendations",
                impact="Run 'ks profile set' to add heroes, gear, buildings",
            )
        )
