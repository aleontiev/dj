import click
from .run import run


@click.command()
def shell():
    """Start the Django shell."""
    run.main(['manage.py', 'shell'])
