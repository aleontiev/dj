import click
from click.exceptions import ClickException
from django_cli.application import get_current_application
from .base import stdout, format_command


@click.argument('args', nargs=-1, type=click.UNPROCESSED)
@click.command(
    context_settings={
        'ignore_unknown_options': True
    }
)
def run(args):
    """Run a command within the app's virtual environment."""
    stdout.write(format_command('Running', ' '.join(args)))
    if not args:
        raise ClickException('pass a command to run')

    args = ' '.join(args)
    application = get_current_application()
    application.run(args, verbose=True, abort=False)
