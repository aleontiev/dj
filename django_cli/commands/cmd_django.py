import click
from django_cli.commands.base import MultiCommand as _MultiCommand


class MultiCommand(_MultiCommand):
    pass


@click.command(cls=MultiCommand)
def command(*args, **kwargs):
    """The Django CLI."""
    pass
