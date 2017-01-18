import os
import click
from .generate import generate
from django_cli.config import Config
from .base import stdout, format_command
from .run import run
from .generate import generate

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

    generate.main(['init', name], standalone_mode=False)
    stdout.write(format_command('Migrating'))
    run.main(['manage.py', 'migrate'])
