import click
from .run import run


@click.command()
def makemigrations():
    """Create new migrations."""
    run.main(['manage.py', 'makemigrations'])
