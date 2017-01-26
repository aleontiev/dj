from __future__ import absolute_import
import click
from .run import run


@click.argument('args', nargs=-1, type=click.UNPROCESSED)
@click.command(
    context_settings={
        'ignore_unknown_options': True
    }
)
def test(args):
    """Run tests."""
    args = [
        'pytest', 'tests', '--ds=tests.settings'
    ] + list(args)
    run.main(args, standalone_mode=False)
