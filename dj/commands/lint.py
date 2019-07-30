from __future__ import absolute_import
import click
from dj.application import get_current_application
from .run import run


@click.argument("args", nargs=-1, type=click.UNPROCESSED)
@click.command(context_settings={"ignore_unknown_options": True})
def lint(args):
    """Run lint checks using flake8."""
    application = get_current_application()
    if not args:
        args = [application.name, "tests"]
    args = ["flake8"] + list(args)
    run.main(args, standalone_mode=False)
