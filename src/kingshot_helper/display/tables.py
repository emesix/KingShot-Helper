from rich import box
from rich.table import Table

from kingshot_helper.engines.gear import EnhanceResult, ForgeResult, MithrilResult
from kingshot_helper.engines.governor import CharmResult, GovGearResult
from kingshot_helper.engines.heroes import ShardResult, XPResult
from kingshot_helper.engines.troops import EventPoints, TrainingCost


def hero_xp_table(result: XPResult) -> Table:
    t = Table(
        title=f"Hero XP: Level {result.current_level} → {result.target_level}",
        box=box.ROUNDED,
    )
    t.add_column("Level", style="cyan", justify="right")
    t.add_column("XP Required", style="green", justify="right")
    for lv, xp in result.breakdown:
        t.add_row(str(lv), f"{xp:,}")
    t.add_section()
    t.add_row("[bold]Total[/]", f"[bold]{result.total_xp:,}[/]")
    return t


def hero_shard_table(result: ShardResult) -> Table:
    t = Table(
        title=f"Hero Shards: {result.current_stars}★ → {result.target_stars}★",
        box=box.ROUNDED,
    )
    t.add_column("Star", style="cyan", justify="right")
    t.add_column("Shards", style="green", justify="right")
    for star, cost in result.per_star:
        t.add_row(f"{star}★", f"{cost:,}")
    t.add_section()
    t.add_row("[bold]Total needed[/]", f"[bold]{result.shards_needed:,}[/]")
    t.add_row("Owned", f"{result.shards_owned:,}")
    color = "green" if result.shards_deficit == 0 else "red"
    t.add_row("Deficit", f"[{color}]{result.shards_deficit:,}[/{color}]")
    return t


def gear_enhance_table(result: EnhanceResult) -> Table:
    t = Table(
        title=(
            f"Gear Enhancement: Level {result.current_level}"
            f" → {result.target_level} ({result.rarity.value})"
        ),
        box=box.ROUNDED,
    )
    t.add_column("Field", style="cyan")
    t.add_column("Value", style="green", justify="right")
    t.add_row("Total XP", f"{result.total_xp:,}")
    t.add_row("Rarity cap", str(result.max_level))
    if result.capped:
        t.add_row("[yellow]Capped[/]", f"[yellow]Target exceeds {result.rarity.value} cap[/]")
    return t


def forge_table(result: ForgeResult) -> Table:
    t = Table(
        title=f"Mastery Forging: Level {result.current_level} → {result.target_level}",
        box=box.ROUNDED,
    )
    t.add_column("Level", justify="right")
    t.add_column("Hammers", justify="right", style="yellow")
    t.add_column("Mythic Gears", justify="right", style="red")
    for entry in result.breakdown:
        mg = str(entry["mythic_gears"]) if entry["mythic_gears"] > 0 else "-"
        t.add_row(str(entry["level"]), str(entry["hammers"]), mg)
    t.add_section()
    t.add_row(
        "[bold]Total[/]",
        f"[bold]{result.total_hammers:,}[/]",
        f"[bold]{result.total_mythic_gears}[/]",
    )
    t.add_row("Stat bonus", f"+{result.stat_bonus_percent:.0f}%", "")
    return t


def mithril_table(result: MithrilResult) -> Table:
    t = Table(
        title=f"Red Gear: Level {result.current_level} → {result.target_level}",
        box=box.ROUNDED,
    )
    t.add_column("Block", style="cyan")
    t.add_column("Mithril", justify="right", style="magenta")
    t.add_column("Mythic Gears", justify="right", style="red")
    for b in result.blocks:
        t.add_row(f"{b['from_level']}→{b['to_level']}", str(b["mithril"]), str(b["mythic_gears"]))
    t.add_section()
    t.add_row(
        "[bold]Total[/]",
        f"[bold]{result.total_mithril}[/]",
        f"[bold]{result.total_mythic_gears}[/]",
    )
    return t


def training_cost_table(result: TrainingCost) -> Table:
    t = Table(
        title=f"Training Cost: {result.count:,}x T{result.tier} {result.troop_type.value}",
        box=box.ROUNDED,
    )
    t.add_column("Resource", style="cyan")
    t.add_column("Amount", style="green", justify="right")
    t.add_row("Bread", f"{result.bread:,}")
    t.add_row("Wood", f"{result.wood:,}")
    t.add_row("Stone", f"{result.stone:,}")
    t.add_row("Iron", f"{result.iron:,}")
    t.add_section()
    t.add_row("[bold]Total[/]", f"[bold]{result.total_resources:,}[/]")
    return t


def event_points_table(result: EventPoints) -> Table:
    t = Table(
        title=f"Event Points: {result.count:,}x T{result.tier} ({result.event.value.upper()})",
        box=box.ROUNDED,
    )
    t.add_column("Field", style="cyan")
    t.add_column("Value", style="green", justify="right")
    t.add_row("Points/unit", f"{result.points_per_unit:,}")
    t.add_row("Total points", f"[bold]{result.total_points:,}[/]")
    t.add_row("Power/unit", f"{result.power_per_unit:,}")
    t.add_row("Total power", f"{result.total_power:,}")
    return t


def gov_gear_table(result: GovGearResult) -> Table:
    t = Table(
        title=(
            f"Governor Gear: {result.current_tier} {result.current_stars}★"
            f" → {result.target_tier} {result.target_stars}★"
        ),
        box=box.ROUNDED,
    )
    t.add_column("Material", style="cyan")
    t.add_column("Needed", justify="right", style="yellow")
    t.add_column("Deficit", justify="right")
    _deficit_row(t, "Satin", result.satin_needed, result.satin_deficit)
    _deficit_row(t, "Gilded Threads", result.threads_needed, result.threads_deficit)
    _deficit_row(t, "Artisan's Vision", result.visions_needed, result.visions_deficit)
    if result.power_at_target:
        t.add_section()
        t.add_row("Power at target", f"{result.power_at_target:,}", "")
    return t


def charm_table(result: CharmResult) -> Table:
    t = Table(
        title=f"Governor Charm: Level {result.current_level} → {result.target_level}",
        box=box.ROUNDED,
    )
    t.add_column("Level", justify="right", style="cyan")
    t.add_column("Guides", justify="right", style="yellow")
    t.add_column("Designs", justify="right", style="magenta")
    for entry in result.breakdown:
        t.add_row(str(entry["level"]), str(entry["guides"]), str(entry["designs"]))
    t.add_section()
    t.add_row(
        "[bold]Total[/]",
        f"[bold]{result.guides_needed:,}[/]",
        f"[bold]{result.designs_needed:,}[/]",
    )
    g_color = "green" if result.guides_deficit == 0 else "red"
    d_color = "green" if result.designs_deficit == 0 else "red"
    t.add_row(
        "Deficit",
        f"[{g_color}]{result.guides_deficit:,}[/{g_color}]",
        f"[{d_color}]{result.designs_deficit:,}[/{d_color}]",
    )
    return t


def _deficit_row(table: Table, label: str, needed: int, deficit: int) -> None:
    color = "green" if deficit == 0 else "red"
    table.add_row(label, f"{needed:,}", f"[{color}]{deficit:,}[/{color}]")
