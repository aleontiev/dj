import click
from django_cli.dependency import Dependency
from django_cli.application import get_current_application
from django_cli.utils import style
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
