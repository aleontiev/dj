import os
import click
from .generate import generate
from django_cli.config import Config
from django_cli.application import Application
from .base import stdout, format_command

@click.command()
@click.argument('name')
@click.option(
    '--runtime',
    prompt=click.style('Python version', fg='yellow'),
    default=Config.defaults['runtime']
)
def init(name, runtime):
    """Create a new Django app in the current directory."""
    stdout.write(format_command('Initializing', '%s on %s' % (name, runtime)))

    config = Config(os.getcwd())
    config.set('runtime', runtime)
    config.save()

    generate.main(['init', name])
