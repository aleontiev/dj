from __future__ import absolute_import
import click
import os
from click.exceptions import ClickException
from djay.application import get_current_application


@click.option("--quiet", is_flag=True, default=False)
@click.argument("args", nargs=-1, type=click.UNPROCESSED)
@click.command(context_settings={"ignore_unknown_options": True})
def run(quiet, args):
    """Run a local command.

    Examples:

    $ django run manage.py runserver

    ...
    """
    if not args:
        raise ClickException("pass a command to run")

    cmd = " ".join(args)
    application = get_current_application()
    name = application.name
    settings = os.environ.get("DJANGO_SETTINGS_MODULE", "%s.settings" % name)
    return application.run(
        cmd,
        verbose=not quiet,
        abort=False,
        capture=True,
        env={"DJANGO_SETTINGS_MODULE": settings},
    )
