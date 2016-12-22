import click
from .generate import generate


@click.command()
@click.argument('name')
def init(name):
    """Create a new Django app in the current directory."""
    generate.main()
