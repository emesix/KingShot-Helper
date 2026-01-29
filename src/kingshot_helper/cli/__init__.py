import typer

app = typer.Typer(
    name="ks",
    help="Kingshot Helper — gameplay advisor CLI",
    no_args_is_help=True,
    rich_markup_mode="rich",
)


def _register_commands() -> None:
    from kingshot_helper.cli import (
        battle,
        buildings,
        events,
        gear,
        governor,
        hero,
        pets,
        profile,
        recommend,
        troops,
    )

    app.add_typer(hero.app, name="hero", help="Hero XP and shard calculations")
    app.add_typer(gear.app, name="gear", help="Gear enhancement, forging, mithril")
    app.add_typer(troops.app, name="troops", help="Troop training costs and event points")
    app.add_typer(buildings.app, name="build", help="Building upgrade planning")
    app.add_typer(governor.app, name="gov", help="Governor gear and charm materials")
    app.add_typer(pets.app, name="pet", help="Pet leveling and advancement")
    app.add_typer(battle.app, name="battle", help="Formation optimizer")
    app.add_typer(events.app, name="event", help="Event point calculators")
    app.add_typer(profile.app, name="profile", help="Player profile management")
    app.command(name="recommend")(recommend.recommend)


_register_commands()
