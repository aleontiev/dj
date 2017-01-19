import click
from django_cli.application import get_current_application
from django_cli.dependency import Dependency
from django_cli.utils import style
from .base import stdout


@click.argument('addon')
@click.option('--dev', is_flag=True)
@click.command()
def add(addon, dev):
    """Add a dependency."""
    stdout.write(style.format_command('Adding', Dependency(addon).to_stdout()))
    application = get_current_application()
    application.add(addon, dev=dev)
