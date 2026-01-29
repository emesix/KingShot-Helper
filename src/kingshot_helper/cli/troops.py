from typing import Annotated

import typer
from rich.console import Console

from kingshot_helper.display.tables import event_points_table, training_cost_table
from kingshot_helper.engines.troops import calc_event_points, calc_training_cost
from kingshot_helper.models.enums import EventType, TroopType

app = typer.Typer(no_args_is_help=True)
console = Console()


@app.command()
def train(
    tier: Annotated[int, typer.Argument(help="Troop tier (1-10)")],
    troop_type: Annotated[TroopType, typer.Argument(help="infantry/archer/cavalry")],
    count: Annotated[int, typer.Argument(help="Number of troops")],
):
    """Calculate resources needed to train troops."""
    result = calc_training_cost(tier, troop_type, count)
    console.print(training_cost_table(result))


@app.command()
def points(
    tier: Annotated[int, typer.Argument(help="Troop tier (1-10)")],
    count: Annotated[int, typer.Argument(help="Number of troops")],
    event: Annotated[EventType, typer.Option(help="Event type")] = EventType.HOG,
):
    """Calculate event points from training troops."""
    result = calc_event_points(tier, event, count)
    console.print(event_points_table(result))
