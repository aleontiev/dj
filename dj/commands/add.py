from __future__ import absolute_import
import click
from dj.application import get_current_application


@click.argument('addon')
@click.option('--dev', is_flag=True)
@click.command()
def add(addon, dev):
    """Add a dependency.

    Examples:

    $ django add dynamic-rest==1.5.0

    + dynamic-rest == 1.5.0
    """
    application = get_current_application()
    application.add(addon, dev=dev)
