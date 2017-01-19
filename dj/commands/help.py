from __future__ import absolute_import
import click
from .run import run


@click.command()
def help():
    """Display usage info."""
    run.main(['--help'])
