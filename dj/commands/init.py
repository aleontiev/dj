from __future__ import absolute_import
import os
import click
from dj.config import Config
from dj.utils import style
from .generate import generate
from .base import stdout
from .run import run


@click.command()
@click.argument('name')
@click.option(
    '--runtime',
    prompt=style.prompt('Python version'),
    default=style.default(Config.defaults['runtime'])
)
def init(name, runtime):
    """Create a new Django app."""
    runtime = click.unstyle(runtime)

    stdout.write(
        style.format_command(
            'Initializing',
            '%s %s %s' % (name, style.gray('@'), style.green(runtime))
        )
    )

    config = Config(os.getcwd())
    config.set('runtime', runtime)
    config.save()

    generate.main(['init', name], standalone_mode=False)
    run.main(['python', 'manage.py', 'migrate'])
