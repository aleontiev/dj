from __future__ import absolute_import
import click
from .run import run


@click.command()
@click.argument("port", required=False)
def server(port):
    """Start the Django dev server."""
    args = ["python", "manage.py", "runserver"]
    if port:
        args.append(port)
    run.main(args)
