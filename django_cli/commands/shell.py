import click
from .run import run
from .base import stdout


@click.command()
def shell():
    """Start the Django shell."""
    run.main(['manage.py', 'shell'])
