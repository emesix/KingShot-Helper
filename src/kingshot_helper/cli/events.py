from typing import Annotated

import typer
from rich import box
from rich.console import Console
from rich.table import Table

from kingshot_helper.engines.events import all_hog_tiers, calc_hog_training, calc_kvk_points

app = typer.Typer(no_args_is_help=True)
console = Console()


@app.command()
def hog(
    tier: Annotated[int, typer.Argument(help="Troop tier (1-10)")] = 10,
    count: Annotated[int, typer.Argument(help="Number of troops")] = 1000,
):
    """Calculate Hall of Governors training points."""
    result = calc_hog_training(tier, count)
    pts = result.total_points
    detail = f"{result.count:,}x T{result.tier} @ {result.points_per_unit} pts/unit"
    console.print(f"[bold]HoG Points:[/] {pts:,} ({detail})")

    console.print("\n[dim]Points per tier reference:[/]")
    t = Table(box=box.SIMPLE)
    t.add_column("Tier", style="cyan", justify="right")
    t.add_column("Pts/unit", style="green", justify="right")
    for row in all_hog_tiers():
        style = "bold" if row["tier"] == tier else ""
        t.add_row(f"[{style}]T{row['tier']}[/{style}]", f"[{style}]{row['hog_points']:,}[/{style}]")
    console.print(t)


@app.command()
def kvk(
    truegold: Annotated[int, typer.Option(help="Truegold bars to use")] = 0,
    speedup_minutes: Annotated[int, typer.Option("--speedups", help="Speedup minutes")] = 0,
    charm_levels: Annotated[int, typer.Option("--charms", help="Charm levels to upgrade")] = 0,
):
    """Estimate KvK preparation phase points."""
    result = calc_kvk_points(truegold, speedup_minutes, charm_levels)
    console.print("[bold]KvK Prep Points Estimate[/]")
    if result.truegold_points:
        console.print(f"  Truegold: {result.truegold_used}x = {result.truegold_points:,} pts")
    if result.speedup_points:
        console.print(f"  Speedups: {result.speedup_minutes} min = {result.speedup_points:,} pts")
    if result.charm_points:
        console.print(f"  Charms: {result.charm_points:,} pts")
    console.print(f"  [bold green]Total: {result.total:,} pts[/]")
