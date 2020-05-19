from __future__ import absolute_import
import click
from .run import run


@click.argument("args", nargs=-1, type=click.UNPROCESSED)
@click.command(context_settings={"ignore_unknown_options": True})
def test(args):
    """Run tests."""
    arguments = []
    options = []
    for arg in args:
        if arg.startswith("--"):
            options.append(arg)
        else:
            arguments.append(arg)

    if not arguments:
        # by default, run all tests
        arguments = ["tests"]

    args = ["pytest"] + arguments + options
    run.main(args, standalone_mode=False)
