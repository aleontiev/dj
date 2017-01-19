import click
from click.exceptions import ClickException
from django_cli.application import get_current_application
from django_cli.utils import style
from .base import stdout


@click.argument('args', nargs=-1, type=click.UNPROCESSED)
@click.command(
    context_settings={
        'ignore_unknown_options': True
    }
)
def run(args):
    """Run a command within the app's virtual environment."""
    stdout.write(style.format_command('Running', ' '.join(args)))
    if not args:
        raise ClickException('pass a command to run')

    cmd = ' '.join(args)
    application = get_current_application()
    name = application.name
    application.run(
        cmd,
        verbose=True,
        abort=False,
        env={
            'DJANGO_SETTINGS_MODULE': '%s.settings' % name
        }
    )
