import click
from click.exceptions import ClickException
from django_cli.application import get_current_application


@click.argument('args', nargs=-1, type=click.UNPROCESSED)
@click.command(
    context_settings={
        'ignore_unknown_options': True
    }
)
def command(args):
    if not args:
        raise ClickException('pass a command to run')

    args = ' '.join(args)
    application = get_current_application()
    application.run(args, verbose=True, abort=False)
