import click
from django_cli.application import get_current_application
from .base import stdout, format_command

@click.argument('addon')
@click.option('--dev', is_flag=True)
@click.command()
def add(addon, dev):
    stdout.write(format_command('Adding', addon))
    application = get_current_application()
    application.add(addon, dev=dev)
