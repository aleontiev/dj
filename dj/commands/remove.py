from __future__ import absolute_import
import click
from dj.dependency import Dependency
from dj.application import get_current_application
from dj.utils import style
from .base import stdout


@click.argument('addon')
@click.option('--dev', is_flag=True)
@click.command()
def remove(addon, dev):
    """Remove a dependency.

    Examples:

    $ django remove dynamic-rest

    - dynamic-rest == 1.5.0
    """
    stdout.write(style.format_command('Removing', Dependency(addon).name))
    application = get_current_application()
    application.remove(addon, dev=dev)
