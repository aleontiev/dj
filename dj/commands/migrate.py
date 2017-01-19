from __future__ import absolute_import
import click
from .run import run


@click.command()
def migrate():
    """Run Django migrations.

    This runs "makemigrations" and "migrate".
    """
    run.main(['manage.py', 'makemigrations'], standalone_mode=False)
    run.main(['manage.py', 'migrate'], standalone_mode=False)
