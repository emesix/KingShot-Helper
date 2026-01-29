from typing import Annotated

import typer
from rich import box
from rich.console import Console
from rich.table import Table

from kingshot_helper.engines.buildings import tc_unlocks

app = typer.Typer(no_args_is_help=True)
console = Console()


@app.command()
def unlocks(
    tc_level: Annotated[int, typer.Argument(help="Current Town Center level")] = 1,
):
    """Show what your Town Center level has unlocked and what's next."""
    info = tc_unlocks(tc_level)
    t = Table(title=f"TC Level {info.current_level} Unlocks", box=box.ROUNDED)
    t.add_column("TC Level", style="cyan", justify="right")
    t.add_column("Feature", style="green")
    for lv, feature in sorted(info.unlocked.items()):
        t.add_row(str(lv), feature)
    if info.next_unlock:
        t.add_section()
        t.add_row(
            f"[bold yellow]{info.next_unlock[0]}[/]", f"[bold yellow]→ {info.next_unlock[1]}[/]"
        )
    console.print(t)
