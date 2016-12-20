import click
from django_cli.commands.base import MultiCommand
from .run import command as run_command
from .init import command as init_command
from .generate import command as generate_command
from .install import command as install_command


class DjangoMultiCommand(MultiCommand):
    commands = {
        'run': run_command,
        'init': init_command,
        'generate': generate_command,
        'install': install_command
    }


@click.command(cls=DjangoMultiCommand)
def command(*args, **kwargs):
    """The Django CLI."""
    pass
