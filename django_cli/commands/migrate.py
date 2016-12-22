import click
from .run import run


@click.command()
def migrate():
    """Run Django migrations."""
    run.main(['manage.py', 'migrate'])
