from typing import Annotated

import typer
from rich.console import Console

from kingshot_helper.display.tables import hero_shard_table, hero_xp_table
from kingshot_helper.engines.heroes import calc_hero_xp, calc_shards, drill_camp_xp

app = typer.Typer(no_args_is_help=True)
console = Console()


@app.command()
def xp(
    current: Annotated[int, typer.Argument(help="Current hero level (0-79)")] = 1,
    target: Annotated[int, typer.Argument(help="Target hero level (1-80)")] = 80,
    verbose: Annotated[
        bool, typer.Option("--verbose", "-v", help="Show per-level breakdown")
    ] = False,
):
    """Calculate total Hero XP needed between two levels."""
    if current >= target:
        console.print("[red]Current level must be less than target.[/]")
        raise typer.Exit(1)
    result = calc_hero_xp(current, target)
    if verbose:
        console.print(hero_xp_table(result))
    else:
        console.print(f"[bold]XP needed:[/] {result.total_xp:,}")
    console.print(f"[dim]TC required for level {target}: {result.tc_required}[/]")
    spillover = drill_camp_xp(result.total_xp)
    console.print(f"[dim]Drill Camp heroes gain: {spillover:,} XP (80% spillover)[/]")


@app.command()
def shards(
    current_stars: Annotated[int, typer.Argument(help="Current star level (0-4)")] = 0,
    target_stars: Annotated[int, typer.Argument(help="Target star level (1-5)")] = 5,
    owned: Annotated[int, typer.Option(help="Shards already owned")] = 0,
    hero_name: Annotated[
        str, typer.Option("--hero", help="Hero name (amadeus/chenko for special costs)")
    ] = "default",
):
    """Calculate shards needed for hero star ascension."""
    if current_stars >= target_stars:
        console.print("[red]Current stars must be less than target.[/]")
        raise typer.Exit(1)
    result = calc_shards(current_stars, target_stars, owned, hero_name)
    console.print(hero_shard_table(result))
