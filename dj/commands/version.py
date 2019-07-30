from __future__ import absolute_import
import click
import pkg_resources
from dj.utils.system import stdout


@click.command()
def version():
    """Display application version."""
    stdout.write(pkg_resources.get_distribution("djay").version)
