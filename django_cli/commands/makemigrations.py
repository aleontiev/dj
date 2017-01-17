import click
from .run import run
from .base import stdout

@click.command()
def makemigrations():
    """Create new migrations."""
    run.main(['manage.py', 'makemigrations'])
