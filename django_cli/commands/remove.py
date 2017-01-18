import click
from django_cli.application import get_current_application
from .base import stdout, format_command

@click.argument('addon')
@click.option('--dev', is_flag=True)
@click.command()
def remove(addon, dev):
    """Remove a dependency."""
    stdout.write(format_command('Removing', addon))
    application = get_current_application()
    application.remove(addon, dev=dev)
