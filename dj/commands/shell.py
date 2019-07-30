from __future__ import absolute_import
import click
from .run import run


@click.command()
def shell():
    """Start the Django shell."""
    run.main(["python", "manage.py", "shell"])
