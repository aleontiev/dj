from __future__ import absolute_import
import click
from dj.utils.system import stdout

VERSION = '0.0.6'


@click.command()
def version():
    """Display application version."""
    stdout.write(VERSION)
