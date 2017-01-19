import click
from django_cli.commands.base import BlueprintLoaderCommand
from jinja2.exceptions import UndefinedError


@click.command(cls=BlueprintLoaderCommand)
def generate(*args, **kwargs):
    """Generate a code stub."""
    pass


@generate.resultcallback()
def generate_callback(context, application=None, blueprint=None, **kwargs):
    """
    Arguments:
        application: represents current application code
        blueprint: represents the blueprint
    """
    if not application:
        raise click.ClickException('Could not locate application')
    if not blueprint:
        raise click.ClickException('Could not locate blueprint')

    try:
        application.generate(blueprint, context)
    except UndefinedError as e:
        raise click.ClickException(
            '%s.\n'
            'The blueprint\'s context may be invalid.' % str(e)
        )
