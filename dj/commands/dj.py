from __future__ import absolute_import
import click

from .base import MultiCommand
from .shell import shell
from .run import run
from .init import init
from .generate import generate
from .add import add
from .remove import remove
from .migrate import migrate
from .server import server
from .test import test
from .info import info
from .help import help


class _MultiCommand(MultiCommand):
    commands = {
        'migrate': migrate,
        'server': server,
        'shell': shell,
        'test': test,
        'run': run,
        'init': init,
        'generate': generate,
        'add': add,
        'remove': remove,
        'info': info,
        'help': help
    }


@click.command(cls=_MultiCommand)
def dj(*args, **kwargs):
    """DJ, the Django CLI."""
    pass


def execute(command):
    command = command.split(' ')
    return dj.main(command, standalone_mode=False)
