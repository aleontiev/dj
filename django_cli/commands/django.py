import sys, os
import click
from django_cli.commands.base import MultiCommand

from .shell import shell
from .run import run
from .init import init
from .generate import generate
from .add import add
from .remove import remove
from .migrate import migrate
from .server import server
from .info import info

class DjangoMultiCommand(MultiCommand):
    commands = {
        'migrate': migrate,
        'server': server,
        'shell': shell,
        'run': run,
        'init': init,
        'generate': generate,
        'add': add,
        'remove': remove,
        'info': info
    }


@click.command(cls=DjangoMultiCommand)
def command(*args, **kwargs):
    """The Django CLI."""
    pass
