from rich import box
from rich.panel import Panel
from rich.table import Table

from kingshot_helper.engines.advisor import Recommendation
from kingshot_helper.engines.battle import FormationAdvice
from kingshot_helper.engines.pets import PetLevelResult
from kingshot_helper.models.profile import UserProfile


def formation_panel(f: FormationAdvice) -> Panel:
    lines = [
        f"[bold cyan]Infantry:[/]  {f.infantry_count:>8,}  ({f.infantry_pct:.0%})",
        f"[bold green]Archers:[/]  {f.archer_count:>8,}  ({f.archer_pct:.0%})",
        f"[bold red]Cavalry:[/]  {f.cavalry_count:>8,}  ({f.cavalry_pct:.0%})",
        "",
        f"[dim]{f.notes}[/]",
    ]
    if f.hero_recommendations:
        lines.append("")
        lines.append("[bold]Recommended heroes:[/] " + ", ".join(f.hero_recommendations))
    return Panel("\n".join(lines), title=f"Formation: {f.mode.value}", border_style="blue")


def pet_panel(result: PetLevelResult) -> Panel:
    lines = [
        f"[bold]Level range:[/] {result.current} → {result.effective_target}",
    ]
    if result.capped:
        lines.append(f"[yellow]Capped at {result.effective_target} (rarity limit)[/]")
    if result.advancements:
        lines.append("")
        lines.append("[bold]Advancement milestones:[/]")
        for adv in result.advancements:
            items = (
                ", ".join(f"{k}: {v}" for k, v in adv["items"].items())
                if adv["items"]
                else "items TBD"
            )
            lines.append(f"  Level {adv['level']}: {items}")
    else:
        lines.append("[dim]No advancements in this range[/]")
    return Panel("\n".join(lines), title="Pet Leveling", border_style="green")


def recommendations_panel(recs: list[Recommendation]) -> Panel:
    t = Table(box=box.SIMPLE)
    t.add_column("#", style="bold", width=3)
    t.add_column("Domain", style="cyan", width=10)
    t.add_column("Action", style="green")
    t.add_column("Impact", style="yellow")
    for i, r in enumerate(recs, 1):
        t.add_row(str(i), r.domain, r.action, r.impact)
    return Panel(t, title="[bold]Top Recommendations[/]", border_style="green")


def profile_panel(p: UserProfile) -> Panel:
    lines = [
        f"[bold]Profile:[/] {p.name}",
        f"[bold]Town Center:[/] {p.town_center_level}"
        + (f" (TG{p.town_center_tg})" if p.town_center_tg else ""),
        f"[bold]Heroes:[/] {len(p.heroes)}",
    ]
    for h in p.heroes:
        gear_count = len(h.gear)
        lines.append(
            f"  {h.name}: Lv{h.level} {h.stars}★ ({h.shards_owned} shards, {gear_count} gear)"
        )
    lines.append(f"[bold]Pets:[/] {len(p.pets)}")
    for pet in p.pets:
        lines.append(f"  {pet.name}: Lv{pet.level} ({pet.rarity.value})")
    lines.append(f"[bold]Governor Gear:[/] {p.governor_gear.tier.value} {p.governor_gear.stars}★")
    lines.append(f"[bold]Governor Charm:[/] Level {p.governor_charm.level}")
    res = p.resources
    lines.append(
        f"[bold]Resources:[/] 🍞{res.bread:,} 🪵{res.wood:,} 🪨{res.stone:,} ⚙{res.iron:,}"
    )
    if res.truegold or res.mithril or res.forgehammers:
        extras = []
        if res.truegold:
            extras.append(f"Truegold: {res.truegold}")
        if res.mithril:
            extras.append(f"Mithril: {res.mithril}")
        if res.forgehammers:
            extras.append(f"Forgehammers: {res.forgehammers}")
        lines.append(f"  {', '.join(extras)}")
    return Panel("\n".join(lines), title="Player Profile", border_style="blue")
