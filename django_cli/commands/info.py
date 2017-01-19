import click
from django_cli.application import get_current_application
from django_cli.utils.system import stdout


@click.command()
def info():
    """Display info."""
    application = get_current_application()
    stdout.write(application.info())
