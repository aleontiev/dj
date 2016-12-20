import click
from django_cli.application import get_current_application


@click.argument('args', nargs=-1, type=click.UNPROCESSED)
@click.command()
def command(args):
    application = get_current_application()
    application.run(' '.join(args))
