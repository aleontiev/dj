from __future__ import absolute_import
import click

from .base import MultiCommand
from .add import add
from .generate import generate
from .help import help
from .info import info
from .init import init
from .lint import lint
from .migrate import migrate
from .remove import remove
from .run import run
from .server import server
from .shell import shell
from .test import test
from .version import version


class _MultiCommand(MultiCommand):
    commands = {
        "add": add,
        "generate": generate,
        "help": help,
        "info": info,
        "init": init,
        "lint": lint,
        "migrate": migrate,
        "remove": remove,
        "run": run,
        "server": server,
        "shell": shell,
        "test": test,
        "version": version,
    }


@click.command(cls=_MultiCommand)
def dj(*args, **kwargs):
    """DJ, the Django CLI."""
    pass


def execute(command):
    command = command.split(" ")
    return dj.main(command, standalone_mode=False)
