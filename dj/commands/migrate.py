from __future__ import absolute_import
import click
from .run import run


@click.command()
def migrate():
    """Run Django migrations.

    This runs "makemigrations" and "migrate".
    """
    run.main(['python', 'manage.py', 'makemigrations'], standalone_mode=False)
    run.main(['python', 'manage.py', 'migrate'], standalone_mode=False)
