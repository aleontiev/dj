import click
from django_cli.application import get_current_application

@click.argument('addon')
@click.option('--dev', is_flag=True)
@click.command()
def add(addon, dev):
    application = get_current_application()
    application.add(addon, dev=dev)
