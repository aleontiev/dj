from __future__ import absolute_import
import click
from dj.application import get_current_application


@click.argument('addon')
@click.option('--dev', is_flag=True)
@click.command()
def remove(addon, dev):
    """Remove a dependency.

    Examples:

    $ django remove dynamic-rest

    - dynamic-rest == 1.5.0
    """
    application = get_current_application()
    application.remove(addon, dev=dev)
