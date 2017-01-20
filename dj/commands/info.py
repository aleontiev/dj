from __future__ import absolute_import
import click
from dj.application import get_current_application
from dj.utils.system import stdout


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
    info = application.info()
    stdout.write(info)
    return info
