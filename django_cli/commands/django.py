import sys, os
import click
from django_cli.commands.base import MultiCommand

from .shell import shell
from .run import run
from .init import init
from .generate import generate
from .add import add
from .migrate import migrate
from .makemigrations import makemigrations
from .runserver import runserver

class DjangoMultiCommand(MultiCommand):
    commands = {
        'migrate': migrate,
        'migrations': makemigrations,
        'server': runserver,
        'shell': shell,
        'run': run,
        'init': init,
        'generate': generate,
        'add': add
    }


@click.command(cls=DjangoMultiCommand)
def command(*args, **kwargs):
    """The Django CLI."""
    pass
