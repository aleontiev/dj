import click
from django_cli.application import get_current_application
from django_cli.utils.system import stdout


@click.command()
def info():
    """Display app info.

    Examples:

    $ django info
    No application, try running django init.

    $ django info
    Application:
      foo @ 2.7.9
    Requirements:
      Django == 1.10

    """
    application = get_current_application()
    stdout.write(application.info())
