from typing import Annotated

import typer
from rich.console import Console

from kingshot_helper.display.panels import formation_panel
from kingshot_helper.engines.battle import recommend_formation
from kingshot_helper.models.enums import BattleMode

app = typer.Typer(no_args_is_help=True)
console = Console()


@app.command()
def bear(
    troops: Annotated[int, typer.Argument(help="Total troops in march")],
):
    """Optimal Bear Hunt formation (80% archers)."""
    result = recommend_formation(BattleMode.BEAR_HUNT, troops)
    console.print(formation_panel(result))


@app.command()
def pvp(
    troops: Annotated[int, typer.Argument(help="Total troops in march")],
):
    """PvP rally formation (balanced)."""
    result = recommend_formation(BattleMode.PVP_RALLY, troops)
    console.print(formation_panel(result))


@app.command()
def garrison(
    troops: Annotated[int, typer.Argument(help="Total troops for garrison")],
):
    """Garrison defense formation (no archers)."""
    result = recommend_formation(BattleMode.GARRISON, troops)
    console.print(formation_panel(result))
