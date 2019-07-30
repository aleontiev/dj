from __future__ import absolute_import
import click


@click.command()
def help():
    """Display usage info."""
    from .dj import dj

    dj.main(["--help"])
