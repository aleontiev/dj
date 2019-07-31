from __future__ import absolute_import
import click
from dj.utils.system import stdout
from dj.version import __version__


@click.command()
def version():
    """Display application version."""
    stdout.write(__version__)
